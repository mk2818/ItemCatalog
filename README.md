Udacity's Full-Stack Nanodegree - Item Catalog Project on AWS
=============================================================

Purpose
-------
This project is a web application that uses a third-party authentication and then displays a list of categories and items within these categories.  Authenticated users can create, update and delete their own items.  `Amazon Web Services (AWS)` will host the instance that has this ItemCategory web application.

Features
--------
* I used PuTTY to access `34.220.153.111` port `2200` as `grader`.
* The IP address and URL is http://34.220.153.111.xip.io/.
* OAuth via Google Sign-in API
* User Authentication and Authorization
* CRUD via SQLAlchemy and Flask
* JSON endpoints
* The `grader` user can log into the server with the SSH key submitted with the project.
* The `grader` user can run commands using `sudo` to inspect files that are readable only by root.
* `root` cannot log in remotely because `/etc/ssh/sshd_config` has `PermitRootLogin no`.
* `https://github.com/mk2818/ItemCatalog` has `client_secrets.json` and this `README.md`.
* Listed below are the software installed and a few of the parameters configured.
  * ufw allow 2200/tcp
  * ufw enable
  * ufw default allow outgoing
  * ufw allow 80
  * ufw allow 123
  * adduser grader
  * vi /etc/sudoers.d/90-cloud-init-users
  * apt-get install apache2
  * apt-get install libapache2-mod-wsgi
  * cat -n index.html
  * cat -n /etc/apache2/sites-enabled/000-default.conf
  * cat -n /var/www/html/myapp.wsgi
  * apt-get install postgresql
  * apt-get install git-core
  * apt-get install python2.7
  * apt-get install python-setuptools
  * easy_install pip
  * pip install werkzeug==0.8.3
  * pip install flask==0.9
  * pip install Flask-Login==0.1.3
  * pip install pyopenssl
  * pip install requests
  * easy_install sqlalchemy
  * pip install passlib
  * pip install itsdangerous
  * apt-get install python-psycopg2
  * pip install Flask-HTTPAuth
  * pip install --upgrade oauth2client
  * pip install virtualenv
  * a2enmod wsgi
  * a2ensite catalog
  * source venv/bin/activate
  * (venv) $ pip install Flask

Third-Party Resources
---------------------
* Connect to AWS Management Console webpage - https://us-west-2.console.aws.amazon.com/console/home?nc2=h_ct&region=us-west-2&src=header-signin#
* Connect to AWS via a different "ssh" port - https://askubuntu.com/questions/1019891/connecting-to-amazon-lightsail-ubuntu-server-using-different-ssh-port
* Add Lightsail To AWS Management Console   - https://lightsail.aws.amazon.com/ls/webapp/us-west-2/instances/Ubuntu-512MB-Oregon-1/networking?#
* Disallow remote access to PostgreSQL      - https://bosnadev.com/2015/12/15/allow-remote-connections-postgresql-database-server/
* Deploy a Flask application on Ubuntu      - https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
* Run a Flask application on AWS            - https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/

Postgres Database Tables
----------------------
The Postgres database has three tables:
* `category` - has "id", "name" and "user_id" columns.
* `item` - has "id", "title", "description", "category_id" and "user_id" columns.
* `user` - has "id", "name", "email" and "picture" columns.

Program Design
--------------
A Python file has the flask routes for URL paths.  These paths will be used in the browsers and will show which functions are called.  The functions will allow the user to list categories, list items in a category, create categories, update or delete categories created by the user, and create, update and delete items in categories created by the user.  The `__init__.py` Python program executed at http://34.220.153.111.xip.io/ starts the Item Catalog app.  The app uses a Postgres `"categoryitem.db` database to store the data for the app.

Zipped Files
------------
`categoryitem.db` is the SQLite database.
`client_secrets.json` is used by the Google Sign-in API.
`lotsofcategoryitems.py` prepopulates the database with categories and items.
`models.py` defines the database structure.
`models.pyc` is the compiled `models.py`.
`README.txt` is this `README.md` file.
`views.py` - is the core program that runs the app.

`templates` Folder
* `catalog.html`        displays the categories and items in categories created by the user.
* `catalogJson.html`    displays all of the data in the database in a JSON format.
* `category.html`       displays all items in a specified category.
* `deleteCategory.html` displays the screen to delete a category.
* `deleteItem.html`     displays the screen to delete an item.
* `editCategory.html`   displays the screen to update a category.
* `editItem.html`       displays the screen to update an item.
* `header.html`         displays the header on every web page.
* `item.html`           displays the specified item.
* `listItem.html`       displays all items created by anyone in a JSON format.
* `login.html`          displays the login screen.
* `main.html`           defines  the main container of the app.
* `newCategory.html`    displays the screen to create a category.
* `newItem.html`        displays the screen to create an item.
* `publiccatalog.html`  displays the catalog.
* `publiccategory.html` displays the category.
* `publicitem.html`     displays the item.

The following html files have the `required` attribute.
When this attribute is set, the form would not submit and will display an error message
when the input is empty.  The input will also be considered invalid.
* `editCategory.html`
* `editItem.html`
* `newCategory.html`
* `newItem.html`

`static` Folder
* blank_user.gif
* styles.css
* top-banner.jpg

Program Execution
-----------------
 1. Click http://34.220.153.111.xip.io/.
 2. Click "Log in" in the upper-right corner of the web page.
 3. Enter password for your Google account.
    If the browser cache has not been cleared,
    then the application will redirect to the home page.
 4. Create a new category.
 5. Create a new item for any category.
 6. Edit the new item created in Step 5.
 7. Edit the new category created in Step 4.
 8. Generate the four JSON output in the right column on the home page.
 9. Delete the new item.
10. Delete the new category.
