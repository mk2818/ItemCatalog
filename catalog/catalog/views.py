from flask import Flask, render_template, redirect, url_for
from flask import flash, jsonify, make_response
from flask import request, g
from flask import session as login_session
from sqlalchemy import create_engine
from functools import update_wrapper
from models import Base, User, Category, Item

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_httpauth import HTTPBasicAuth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string

import requests
import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

auth = HTTPBasicAuth()

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# engine = create_engine('sqlite:///categoryitem.db',
#                        connect_args={'check_same_thread': False})
engine = create_engine('postgresql://catalog:mypass@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
          json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Assing Email as name if User does not have Google+
    if "name" in data:
        login_session['username'] = data['name']
    else:
        name_corp = data['email'][:data['email'].find("@")]
        login_session['username'] = name_corp
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Check if the user is already logged in
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; \
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions


def createUser(login_session):
    newUser = User()
    newUser.name = login_session['username']
    newUser.email = login_session['email']
    newUser.picture = login_session['picture']

    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except AttributeError:
        return None


# DISCONNECT Google
# Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Log out the currently connected user.
@app.route('/disconnect')
def disconnect():
    if 'username' not in login_session:
        # user IS NOT logged in
        flash('You are not logged in to begin with!')
        redirect(url_for('showCatalog'))
    else:
        # user IS logged in
        gdisconnect()

        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have sucessfully been logged out.")
        return redirect(url_for('showCatalog'))


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


# CATALOG
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).all()
    last_five_items = reversed(session.query(Item).all()[-5:])

    # is user logged in?
    #   - NO,  show user public page
    #   - YES, show user logged in page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        return render_template('publiccatalog.html',
                               categories=categories, items=last_five_items)
    else:
        userCategories = session.query(Category).filter_by(
            user_id=getUserID(login_session['email'])).all()

        # user IS logged in
        return render_template('catalog.html', categories=categories,
                               items=last_five_items,
                               userCategories=userCategories)


"""
    ******************
    * JSON Functions *
    ******************
"""


# CATALOG - JSON
@app.route('/catalog.json')
def catalogJSON():
    categories = session.query(Category).all()

    # define tab values for each level in the json
    tab = '&nbsp;&nbsp;&nbsp;'
    tab2 = tab+tab
    tab3 = tab2+tab
    tab4 = tab3+tab
    tab5 = tab4+tab

    # number of categories
    # used to determine the starting and closing brackets for categories
    categorycount = 0

    # number of items used in each category
    # used to determine the starting and closing brackets for items
    itemcount = 0

    # create the json which is sent to the browser
    output = '{<br/>'
    output += '%s"Category": [<br/>' % tab

    for category in categories:
        if categorycount > 0:
            if itemcount > 0:
                # close the last item set
                output += '%s}<br/>' % tab4
                output += '%s]<br/>' % tab3

            # close the last category
            output += '%s},<br/>' % tab2

        categorycount += 1

        output += '%s{<br/>' % tab2
        output += '%s"id": %s<br/>' % (tab3, category.id)
        output += '%s"name": %s<br/>' % (tab3, category.name)

        itemcount = 0
        items = session.query(Item).filter_by(category_id=category.id).all()

        for item in items:
            # starting bracket for all items
            if itemcount == 0:
                output += '%s"Item": [<br/>' % tab3

            # closing item bracket for the previous item
            if itemcount > 0:
                output += '%s},<br/>' % tab4

            itemcount += 1
            output += '%s{<br/>' % tab4
            output += '%s"category_id": %s<br/>' % (tab5, item.category_id)
            output += '%s"description": "%s"<br/>' % (tab5, item.description)
            output += '%s"id": %s<br/>' % (tab5, item.id)
            output += '%s"title": "%s"<br/>' % (tab5, item.title)

    # closing item bracket
    if itemcount > 0:
        output += '%s}<br/>' % tab4
        output += '%s]<br/>' % tab3

    # closing category bracket
    output += '%s}<br/>' % tab2
    output += '%s]<br/>' % tab
    output += '}<br/>'

    return output


# CATEGORY - JSON
@app.route('/category.json')
def categoryJSON():
    """ Return JSON of all categories in the catalog """
    categories = session.query(Category).order_by(Category.id.desc())
    return jsonify(Category=[category.serialize for category in categories])


# ITEM - JSON
@app.route('/item.json')
def itemJSON():
    """ Return JSON of all items in the catalog """
    items = session.query(Item).order_by(Item.id.desc())
    return jsonify(Item=[item.serialize for item in items])

# ONE ITEM - HTML
@app.route('/itemlist')
def itemlist():
    """ Return a list of all items """
    # is user logged in?
    #   - NO,  show user public page
    #   - YES, show user logged in page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        return render_template('publicCatalog.html', category_name=category_name,
                           count=count, categories=categories, items=items)
    else:
        items = session.query(Item).all()

    return render_template('listItem.html', items=items)
	
# ONE ITEM - JSON
@app.route('/itemlist.json/<int:item_id>')
def itemlistJSON(item_id):
    """ Return JSON of one item in the catalog """
    items = session.query(Item).filter_by(id=item_id).all()
    return jsonify(Item=[item.serialize for item in items])

"""
    **********************
    * Category Functions *
    **********************
"""


# CATALOG ITEMS
@app.route('/catalog/<string:category_name>/items', methods=['GET'])
def showCatalogItems(category_name):

    # check if category:
    #   - was entered by the user
    #   - exists
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        categories = session.query(Category).all()
        items = session.query(Item).filter_by(category_id=category.id).all()
        count = session.query(Item).filter_by(category_id=category.id).count()
    except AttributeError:
        flash("catalog %s does not exist" % category_name)
        return redirect(url_for('showCatalog'))

    # is user logged in?
    #   - NO,  show user public page
    #   - YES, show user logged in page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        return render_template('publicCatalog.html', category_name=category_name,
                           count=count, categories=categories, items=items)
    else:
        userItems = session.query(Item).filter_by(
            user_id=getUserID(login_session['email'])).all()

    return render_template('category.html', category_name=category_name,
                           count=count, categories=categories, items=items,
                           userItems=userItems)


# NEW CATEGORY
@app.route('/catalog/category/new', methods=['GET', 'POST'])
def newCategory():

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    categories = session.query(Category).all()
    last_five_items = reversed(session.query(Item).all()[-5:])

    if request.method == 'POST':
        # check if user cancelled the add
        if request.form['submit'] == 'cancel':
            flash('Recieved cancel request. New category not created.')
            return redirect(url_for('showCatalog'))

        # check Null or Blank entries entered
        # cannot save to database if no values are entered
        if request.form['name'].strip() == "":
            flash("Error: Please enter a values. Name is required!")
            return render_template('newCategory.html', flash=flash)

        # check if the item already exists in the database
        if session.query(Category).filter_by(
                name=request.form['name']).first() is not None:
            flash(request.form['name'] + " already exists. It cannot be \
                    created.")
            return render_template('newCategory.html', flash=flash)

        # add the new item in the database
        newCategory = Category(
            name=request.form['name'],
            user_id=getUserID(login_session['email']))
        session.add(newCategory)
        session.commit()
        flash(request.form['name'] + " has been created!")

        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')


# EDIT CATEGORY
@app.route('/catalog/category/<string:category_name>/edit',
           methods=['GET', 'POST'])
def editCategory(category_name):

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        editedCategory = session.query(Category).filter_by(
            name=category_name).one()
    except AttributeError:
        flash("Category does not exist")
        return redirect(url_for('showCatalog'))

    # check if user created this category, if NOT redirect to catalog page
    user_id = getUserID(login_session['email'])
    if user_id != category.user_id:
        flash('Unauthorized Access: You do not have access to edit the %s \
              category' % category_name)
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':

        # check if user cancelled the edit
        if request.form['submit'] == 'cancel':
            flash('Received cancel request. Category not edited.')
            return redirect(url_for('showCatalog'))

        if isBlankOrNull('category', editedCategory):
            flash("Error: Cannot have blank fields. Enter a category name.")
            return redirect(url_for('editCategory'))

        # set the editedCategory to the values from the page
        if request.form['name'] != category.name:
            editedCategory.name = request.form['name']

        session.add(editedCategory)
        session.commit()
        flash("Category has been edited!")
        return redirect(url_for('showCatalog'))

    else:
        return render_template('editCategory.html',
                               category_name=category.name)


# DELETE CATEGORY
@app.route('/catalog/category/<string:category_name>/delete',
           methods=['GET', 'POST'])
def deleteCategory(category_name):

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        categoryToDelete = session.query(Category).filter_by(
                            name=category_name).one()
    except AttributeError:
        flash("Category does not exist")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':

        # check if user cancelled the delete
        if request.form['submit'] == 'cancel':
            flash('Received cancel request. Category not deleted.')
            return redirect(url_for('showCatalog'))

        session.delete(categoryToDelete)
        session.commit()
        flash("Category has been deleted!")
        return redirect(url_for('showCatalog'))

    else:
        return render_template('deleteCategory.html',
                               category_name=category.name)


"""
    ******************
    * Item Functions *
    ******************
"""


# SHOW ITEM DESCRIPTION
@app.route('/catalog/<string:category_name>/<string:item_name>',
           methods=['GET'])
def showItemDescription(category_name, item_name):

    try:
        category = session.query(Category).filter_by(name=category_name).one()
        item = session.query(Item).filter_by(title=item_name).one()
    except AttributeError:
        flash("The category or item does not exist")
        return redirect(url_for('showCatalog'))

    # is user logged in?
    #   - NO,  show user public page
    #   - YES, show user logged in page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        return render_template('publicitem.html', item=item)

    try:
        userCategories = session.query(Category).filter_by(
                            user_id=getUserID(login_session['email'])).all()
        userItems = session.query(Item).filter_by(user_id=getUserID(
                        login_session['email'])).all()
    except AttributeError:
        # no user defined items
        userItems = {'title': 'none'}

    # check if category and item:
    #   - were entered by the user
    #   - exists
    if item.category_id != category.id:
        flash(item_name + " does not belong to the " +
              category_name + " category")
        return redirect(url_for('showCatalog'))

    # user IS logged in
    return render_template('item.html', item=item, userItems=userItems)


# NEW ITEM
@app.route('/catalog/item/new', methods=['GET', 'POST'])
def newItem():

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    categories = session.query(Category).all()

    if request.method == 'POST':
        # check if user cancelled the add
        if request.form['submit'] == 'cancel':
            flash('Received cancel request. New item not created.')
            return redirect(url_for('showCatalog'))

        # add the new item in the database
        newItem = Item(
            title=request.form['title'],
            description=request.form['description'],
            category_id=request.form['category_id'],
            user_id=getUserID(login_session['email']))

        # check Null or Blank entries entered
        # cannot save to database if no values are entered
        if isBlankOrNull('edit', newItem):
            flash("Error: Please enter values. All fileds are required!")
            return render_template('newItem.html', categories=categories)

        # check if the item already exists in the database
        if session.query(Item).filter_by(title=request.form[
                                         'title']).first() is not None:
            flash(newItem.title + " already exists. It cannot be created.")
            return render_template('newItem.html', categories=categories,
                                   flash=flash)

        session.add(newItem)
        session.commit()
        flash(request.form['title'] + " has been created!")

        return redirect(url_for('showCatalog'))

    else:
        return render_template('newItem.html', categories=categories)


# EDIT ITEM
@app.route('/catalog/item/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    try:
        item = session.query(Item).filter_by(title=item_name).one()
        editedItem = session.query(Item).filter_by(title=item_name).one()
        categories = session.query(Category).all()
    except AttributeError:
        flash('Cannot edit an item that does not exist.')
        return render_template('editItem.html', item=item,
                               categories=categories)

    if request.method == 'POST':

        # check if user cancelled the edit
        if request.form['submit'] == 'cancel':
            flash('Received cancel request. Item not edited.')
            return redirect(url_for('showCatalog'))

        if isBlankOrNull('edit', editedItem):
            flash("Error: Cannot have blank fields. Enter values.")
            return redirect(url_for('showCatalog'))

        # set the editedItem to the values from the page
        if request.form['title'] != item.title:
            editedItem.title = request.form['title']
        if request.form['description'] != item.description:
            editedItem.description = request.form['description']
        if request.form['category_id'] != item.description:
            editedItem.category_id = request.form['category_id']

        session.add(editedItem)
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('showCatalog'))

    else:
        return render_template('editItem.html', item=item,
                               categories=categories)


# DELETE ITEM
@app.route('/catalog/item/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(item_name):

    # is user logged in, if NOT direct user to login page
    access_token = login_session.get('access_token')
    if access_token is None:
        # user IS NOT logged in
        flash("Unauthorized Access. Login to access other pages of the app.")
        return redirect('/login')

    # user IS logged in
    try:
        item = session.query(Item).filter_by(title=item_name).one()
        itemToDelete = session.query(Item).filter_by(title=item_name).one()
    except AttributeError:
        flash("Error: Cannot delete an item that does not exist")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':

        # check if user cancelled the delete
        if request.form['submit'] == 'cancel':
            flash('Received cancel request. Item not deleted.')
            return redirect(url_for('showCatalog'))

        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('showCatalog'))

    else:
        return render_template('deleteItem.html', item=item)


# Catalog Helper Functions


def isBlankOrNull(item_or_category, item_or_catory_modified):
    if item_or_category == 'category':
        # this comparison is for categories
        try:
            request.form['name']
        except AttributeError:
            return True

        if request.form['name'].strip() != "":
            return False

        return True

    else:
        # this comparison is for items
        try:
            request.form['title']
            request.form['description']
        except AttributeError:
            return True

        if request.form['title'].strip() != "":
            if request.form['description'].strip() != "":
                return False

        return True


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
