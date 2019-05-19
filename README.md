Udacity's Full-Stack Nanodegree - Item Catalog Project
======================================================

Purpose
-------
This project is a web application that uses a third-party authentication and then displays a list of categories and items within these categories.  Authenticated users can create, update and delete their own items.

Features
--------
* OAuth via Google Sign-in API
* User Authentication and Authorization
* CRUD via SQLAlchemy and Flask
* JSON endpoints

Software Required
-----------------
* `Git Bash Terminal` views ".py" and ".md" files.
* `VirtualBox` runs the virtual machine (VM).
* `Vagrant` configures the VM and shares files between the host computer and the VM's filesystem.
* `Python 2` is the programming language for writing the source code for
   this project.

SQLite Database Tables
----------------------
The SQLite database has three tables:
* `category` - has "id", "name" and "user_id" columns.
* `item` - has "id", "title", "description", "category_id" and "user_id" columns.
* `user` - has "id", "name", "email" and "picture" columns.

Install Git (Git Bash Terminal).
--------------------------------
1. Download it from [Git](https://git-scm.com/downloads).
2. Install the version for your operating system.

Install Python 2.
---------------
1. Download it from [Python](https://www.python.org/downloads).
2. Install the version for your operating system.

Install VirtualBox.
-------------------
1. Download it from [VirtualBox](www.virtualbox.org).
2. Install the platform package for your operating system without the extension pack or SDK.

Install Vagrant.
----------------
1. Download it from [Vagrant](https://www.vagrantup.com/downloads.html).
2. Install the version for your operating system.
3. Note that you will be asked to grant network permission to
    Vagrant or to make a firewall exception.

Download VM configuration for VirtualBox.
-----------------------------------------
1. Clone the [Git repository](http://github.com/udacity/fullstack-nanodegree-vm)  to your computer.

Program Design
--------------
A Python file has the flask routes for URL paths.  These paths will be used in the browsers and will show which functions are called.  The functions will allow the user to list categories, list items in a category, create categories, update or delete categories created by the user, and create, update and delete items in categories created by the user.  The `views.py` Python program executed at the vagrant command prompt starts the Item Catalog app.  The app uses a SQLite `"categoryitem.db` database to store the data for the app.

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
1. Verify that Git, Python 2, VirtualBox and Vagrant are installed.
2. Save and extract `Udacity_FullStack_Project02_MiltonKwock.zip`.
3. Open Git Bash.
4. Navigate to the `Udacity_FullStack_Project02_MiltonKwock/vagrant` folder.
5. Type `vagrant up` to start VirtualBox and to configure the VM.
6. Type `vagrant ssh` to log into vagrant.
7. Type `cd /vagrant/catalog`.
8. Execute the following commands to install software needed to run the app.
    a. `sudo pip install werkzeug==0.8.3`
    b. `sudo pip install flask==0.9`
    c. `sudo pip install Flask-Login==0.1.3`
    d. `sudo pip install pyopenssl`
    e. `sudo pip install requests`
9. Type `python models.py` to create the database.
10. Type `python lotsofcategoryitems.py` to populate the database with
    categories and items.
11. Type `python views.py` to start the app.
12. Open a web browser.
13. Type the `http://localhost:8000/` URL.
14. Press "Ctrl-C" to exit from the app.
15. Type "exit" to exit from the VM.
16. Type "vagrant halt" to power off the VM.
17. Type "exit" to exit from Git.
