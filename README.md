# Rental
#### Video Demo:
### Distinctiveness and Complexity:

"Rental" is a platform where You can find and rent any type of transport, or rent out your own transport.

"Rental" is a web application with mobile-responsive design, based on the next libraries and technologies: Python, Django (8 models, 4 forms), HTML, CSS, JavaScript, DOM, jQuery, React, Bootstrap, SQL. It's fundamentally different from previous projects in CS50's Web program. 

Using this app You can:
- View all available for renting transport.
- Find rent offers in a particular region and necessary dates.
- Filter and order offers by all parameters.
- View details about chosen transport and its owner.
- Rent transport and leave your rate with a comment about the owner.
- Create a database of users (owners and customers).

The application can be used as a part of a bigger project or evolve separately by growing functionality and assortment. 

### Installation:
1. Download and install [Python](https://www.python.org/downloads/).
2. Unzip the "Rental.zip" file to the working folder.
3. Open the "Rental" folder in the terminal by following commands:
```
1) $ cd (path to saved Rental folder)
2) $ cd Rental
```
4. Enter `pip install -r requirements.txt` to install/update all necessary libraries.

### Understanding:
In project’s main directory You will see next folders and files:
1. `requirements.txt` - includes information about necessary libraries.
2. `README.md` - You currently reading file.
3. `manage.py` - Django managing code.
4. `db.sqlite3` - the database used by application.
5. `reservation` - folder with Django project settings files.
6. `media` - folder with images uploaded by users. 
7. `transport` - folder, which includes application files.

In `transport` folder You can find:
1) `migrations` folder with database migrate files;
2) `static/transport` folder which includes js, css and icons files;
3) `templates/transport` folder with application's HTML-tamplates;
4) `admin.py` - admin page settings file;
5) `apps.py` - application configurations file;
6) `forms.py` - separately created file for storing all forms used in app;
7) `models.py` - file for storing models objects
8) `tests.py` - file where written some logical tests for application
9) `urls.py` - file which defines URL-path and activated function;
10) `views.py` - file which determines and render application responses.

### Easy Start:
At the moment application doesn't upload to the server. So You need to start it using the Django command.

1. Open the "Rental" folder in the terminal by following commands:
```
1) $ cd (path to saved SDPC folder)
2) $ cd Rental
```
2. Run server. In the command line type:
```
$ python manage.py runserver
```
3. Further to the received link (`http://127.0.0.1:8000/`).

### Design:
The design was developed with mentioned of last UIX tendentious. 
All pages and blocks have a mobile-responsive design and will be correctly screened on any device.

### Usage:
#### Log in page:
The first page, which You will see, will be "Log in" page.

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/Login.JPG)

You have no user account yet, so you need to click on `Regisrer` in the header of the page, and pass registration. Once all necessary information becomes filled, application updates the "users" table in the database and create a new special table for registered user, into which will be inserted its calculation history.

After registration, You will be redirected to the "Log in" page.
Enter your username/password and click the `Log in` button!

#### Main page:
If successfully logged in, You will be redirected to the "main" page.

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/main.JPG)
On the main page, You will see a welcome message and `CALCULATE` button, as buttons in the header of the page. Click `CALCULATE` to start!

#### Calculate page:
After clicking 'CALCULATE' bottom, You will see the next page:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/0c04ca0a6cfee9c9c40684e18f3c1afb07cb3903/screenshots/Calculate.JPG)

On this page, You should choose all options for your new door. Options of selections got directly from the database, so don't try to change It here. JavaScript code makes this page more interactive, so You can see all parameters and doors view before as `Calculate` button will be pushed.
Click 'Calculate'!

When 'Calculate' pressed, the application automatically make the next operations: 
1. Creates an order number and estimated installation date.
2. Calculate door price based on chosen parameters and database price information. 
3. Updates the user's history table.
4. Fills prepared '.xlsx' form.
5. Creates offer's pdf file from this '.xlsx' form and saves it in the pdf-archive folder
6. Redirect You to the "Calculated" page, where You could see chosen parameters, calculated price, and "Print" button. 

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/calculated2.JPG)

Once click "Print", the application gets created earlier file from pdf-archive, which You can print out or save to your device.

### History page:
If click on the "History" in the header, You will see next:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/History.JPG)

This page shows your offer history from the database history table.
Click on the highlighted offer number to get pdf file from the pdf-archive folder.

### Insert New page:
Although, You can insert new information into the doors catalogs. 
For this operation, You have to Log Out and Log in like 'Adminitraror':
```
Username: Admin
Password: 11111111
```
Then, if click on the 'Insert New' in the page header, returns back next page:

![alt text](https://raw.githubusercontent.com/Leongard91/SDPC/main/screenshots/Insert.JPG)

Here You can choose the catalog, what You want to update, and enter all necessary information. Using JavaScipt code, the page shows You can be updated inputs only. 

Into some catalogs, You can insert positions title, price, and even upload images.
Application takes an image in '.png' format, rename and save it in '/static/img' folder.
You don't have png? Try '.jpg' format! The application automatically converts the jpg to png and does some operations.

### Access:
The "SDPC" application is opened for anybody and available on my GitHub page: [Leongard91/SDPC](https://github.com/Leongard91/SDPC)

Database information based on [STRAJ](straj.ua) company page.

Enjoy!