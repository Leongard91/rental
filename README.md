# Rental
#### Video Demo: https://youtu.be/4S0UPUmRkbE
### Distinctiveness and Complexity:

"Rental" is a platform where You can find and rent any type of transport, or rent out your own transport.

"Rental" is a web application with mobile-responsive design, based on the next libraries and technologies: Python, Django (8 models, 4 forms), HTML, CSS, JavaScript, DOM, jQuery, React, Bootstrap, SQL. It's fundamentally different from previous projects in CS50's Web program. 

Using this app You can:
- View all available for renting transport.
- Find rent offers in a particular region and necessary dates.
- Filter and order offers by all parameters.
- View details about chosen transport and its owner.
- Rent transport and leave your rate with a comment about owner.
- Create a database of users (owners and customers).

The application can be used as a part of a bigger project or evolve separately by growing functionality and assortment. 

### Installation:
1. Download and install [Python](https://www.python.org/downloads/).
2. Unzip the "rental.zip" file to the working folder.
3. Open the "rental" folder in the terminal by following commands:
```
1) $ cd (path to saved rental folder)
2) $ cd rental
```
4. Enter `pip install -r requirements.txt` to install/update all necessary libraries.

### Understanding:
In project’s main directory You will see next folders and files:
1. `requirements.txt` - includes information about necessary libraries.
2. `README.md` - You currently reading file.
3. `manage.py` - Django managing code.
4. `db.sqlite3` - the database used by application.
5. `screenshorts` - folder with screenshorts for README.md file.
5. `reservation` - folder with Django project settings files.
6. `media` - folder with images uploaded by users. 
7. `transport` - folder, which includes application files.

In `transport` folder You can find:
 - `migrations` folder with database migrate files;
 - `static/transport` folder which includes js, css and icons files;
 - `templates/transport` folder with application's HTML-tamplates;
 - `admin.py` - admin page settings file;
 - `apps.py` - application configurations file;
 - `forms.py` - separately created file for storing all forms used in app;
 - `models.py` - file for storing models objects
 - `tests.py` - file where written some logical tests for application
 - `urls.py` - file which defines URL-path and activated function;
 - `views.py` - file which determines and render application responses.

### Easy Start:
At the moment application doesn't upload to the server. So You need to start it using the Django command.

1. Open the "Rental" folder in the terminal by following commands:
```
1) $ cd (path to saved rental folder)
2) $ cd rental
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

#### ALL OFFERS page:
The first page, which You will see, will be "ALL OFFERS" page.

![ALL OFFERS page](https://github.com/Leongard91/rental/blob/main/screenshots/index_screenshot.JPG)
On the top of the page You will see header with navigation links, project logo and some search fields. Let's scroll down for now! On the main part of the page appears some cards. This is an offers cards for all transport, which can be rented on this platform. Static `index.js` file downloads 10 offers every time when You reach the bottom of the page. On each card, You can find major information about offers like title, price per day, owner rating, passenger and baggage capacity, transport gearbox type and air conditioner attending. 

##### Order buttons
Upper from offers zone are buttons by which You can define an order off offers appearing: by Newest, Cheapest or Best owners ratings.

##### Search buttons and fields
Clicking to the `See more` button takes You to the `search` page with the same offers.
In the header's search field You can find ready-to-use transport in a particular location and desired dates.

##### DETAIS button
`DETAILS` button on offer card available only for registered users, so once be clicked, You will be redirected to the login page. If You allready logged in, You will see `details` page of chosen offer. 


#### LOG IN page:
After clicking on `LOG IN` button on the page header, "Login" page will be screened.

![Log in page]()

You have no user account yet, so you need to click on `Regisrer` in the header of the page or under login button, and pass registration. Once all necessary information becomes filled, application updates the "User" model and use enterede information for user page.

After registration, You will be logged in and redirected to the "ALL OFFERS" page.
Let's log in and take a look to the "search" page.


#### SEARCh page:
After choosing location and dates on any page, click to the `SEARCH` button. It will generate GET request and show You the `search` page with filtered information.

![Search page]()

On this page we can see two big blocks: "Filter" and "Your search results". In the first block You will see checkboxes, using which You have ability to filter offers in "Your search results" block by transport "Type" and "Category", without reloading the whole page. When You change filters, "Price range" changes too.

Let's choose some offer and click on the `DETAILS` button.


#### DETAILS page:
After clicking 'DETAILS' bottom, You will see the next page:

![DETAILS page]()

On this page, You have ability to read all information about transport, including its short description. To actually rent chosen transport, You should complete filing of the "Order details" form below and click the `BOOK NOW` button. The application validates entered information, inserts it into the database, and sends contact instructions to the transport owner. Then You will be redirected to the `SUCCESS` page.

Congratulations! You have rented transport. Please, wait for the owner's call to hear other information.


### CREATE OFFER page:
If You logged in, `CREATE OFFER` and `PROFILE` links will be available on the top of the header.
Click `CREATE OFFER` to see the New Transport form. 

![CREATE OFFER page]()

To create a new offer and become "owner" You should complete all information in the form. Choosing the transport's photo, and click the `Add` button.
The application brings entered information through next steps:
1. Image saving:
- creates new fone image in a particular size and format;
- resize and put uploaded photo in the center of created fone;
- creates user's folder in media root;
- saves the converted photo in user's folder;
- saves path to this photo in the database.
2. Gets from "POST" request other information, validates, and inserts it into the db.
3. Sends back confirmation "SUCCESS" message. 

Congratulations! You "owner" from now.

### USER page:
Clicking to the "PROFILE" link in the header or owner name in the offer takes You to the chosen user's page, where You could see all information about that user.

![USER page]()

This page shows:
- user rating, work area location, joiner date, and some introduction text; 
- all user's offers;
- all reviews on this user with rates.

You have the ability to leave your own feedback on this user by clicking `Leave Your review >>` link, so don't lose your chance!

### ADMIN page:
Although, You can insert new information into the Type, Category, or any other table in the database. 
For this operation, You have to Log Out, folow to `http://127.0.0.1:8000/admin` and Log in like 'Adminitraror':
```
Username: admin
Password: 1
```
That will open to You The Django admin application page, where You have the ability to change any table's data what You want.

![ADMIN page]()


### ACCESS:
The "Rental" application is opened for anybody and available on my GitHub page: [Leongard91/rental](https://github.com/Leongard91/rental)

Enjoy!
