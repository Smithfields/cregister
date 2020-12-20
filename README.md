Bonjour, nous nous étions entendu durant le cours. Et ainsi, au lieu de faire une interface graphique, je me suis employé à rendre l'application REST Compliant avec la librarie Flask
#Cash Register Python App
###partial REST application, Object Oriented and MVC compliant
Original sources were translated into object oriented code and completely adapted for this different approach.
Among the changes, the app now supports DB request for potentially non-existing ID. Newly created rows also return their ID, which is useful to initialize other object (Purchase_Detail). Some static methods were also added to ease with DB digging. 
I wanted to do REST but I also wanted the app not to request a REST client, so where so method could be pure GET/POST/PUT I switched for a GET/POST + html form approach. However 'menu/all' and 'employee/all' can return both XML or JSON.  
Errors and messages are logged rather than print. Each Database operation is logged as 'DEBUG'

Most static variables are located in the conf/config.py script (non-template forms, sql query, time format, database path, etc. )

>This app checks for user input before writings to db, but doesn't check for what it reads from DB

App Structure:
- — Package **conf**
- / — — > config.py
- / — — > utilities.py
- / — — > config.py


- — Package **mvc**:
- / — — > controller.py
- / — — > model.py
- / — — > view.py


- — Directory **data**:
- / — — > meals.db


- — Directory **template**:
- / — — > empl_edit.html
- / — — > menu_edit.html
- / — — > index.html

>***Cash Register was developed using Venv, PiP, PyCharm Professional 2020.3 under Python v. 3.8***
## **App entry point**
app.py registers @simple_page annotation, it is located in mvc.view and allows Flask to see all the routes. The mvc.view doesn't know DB and relies on mvc.controller which manipulates the mvc.model and both talk directly with the DB Wrapper.
My intention was to only initialize one DB Wrapper and connection for the whole application, unfortunately, so far, I haven't found a way to make it work. 

## **Object model manipulation:**
There are four 'model' classes for each data domain: Employee, Menu, Purchase, Purchase_Detail
Each inherit the class named "Parent_Data" which implement basic and abstract access to a database, parent class is also responsible for cursor management

Fetch - automatically handle cursor\
Execute - manual cursor handling

For an update a fetch must occur on the object before actually updating/saving it

A new Employee can be saved like this:\
`e = Employee(Datasource)`\
`e.f_name = 'Tom'`\
`e.save()`\
or\
`e = Employee(Datasource)`\
`e.save({'f_name': 'Tom'})`\
or (preferably) using actual validation\
`e.validate({'f_name': 'Tom, 'l_name': 'Petty', 'email': 'me@me.m'})`\
`if e: e.save()`\
Validate function will check each field and type, fully populate the object and will do DB Constraint check. Returns False if mandatory parameter is missing or if a type is wrong. Return the object if all went well

All items can be fetch usind the following static method\
`Menu.fetch_all(Datasource)`\
`Employee.fetch_all(Datasource)`\
One item can be update writing\
`m = Menu(Datasource)`\
`m.fetch(1)`\
`m.update({price: 10.5})`\
or\
`m.update({descr:'veggie', price: 10.5})`\
or (preferably)\
`m.validate({descr:'veggie', price: 10.5})`\
`m.update()`
## **Purchase**
Given the REST nature of this app, menu cannot be added to a purchase in a sequence but all provided at once in the purchase by ID (1,4,12). 
Any past purchase can be visualized as json or xml using `/purchase/<id>` url with option fragment `?xml=1`

Any past purchase can also have its receipt computed and printed using the following url `/receipt/<id>`.

>**Note that receipt are downloaded as pdf file directly from the browser!**

## **The following routes are available for partial REST/Form:**
A set of HTML forms have been added in order to dig the application without requiring a REST client. It will accept either GET or POST methods or both

`/employee/look` —> input ID in form > return matching employee as json\
`/employee/all (json|xml)` — > return all employees as json\
`/employee/add` — > html form to add employee > return newly created employee as json\
`/employee/edit/<id>` — > fetch employee based on its id > popuate html form with it > return updated employee as json

`/menu/look`\
`/menu/all (json|xml)`\
`/menu/add`\
`/menu/edit/<id>`

`/purchase/<id> (json|xml)`\
`/purchase/add`

`/receipt/<id>`\
