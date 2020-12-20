#Cash Register Python App
###partial REST application, Object Oriented and MVC compliant
Original sources were translated into object oriented code AND completely adapted for this different approach.
Errors and messages are logged rather than print. Each Database operation is logged as 'DEBUG'

All static variables are located in the conf/config.py script (non-template forms, sql query, time format, database path)

This app checks for user input before writings to db, but doesn't check for what it reads from DB

*Cash Register was developed using Venv, PiP, PyCharm Professional 2020.3 under Python v. 3.8*
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
or\
`m.validate({descr:'veggie', price: 10.5})`\
`m.update()`

## **The following routes are available for partial REST:**
A set of HTML forms have been added in order to dig the application without requiring a REST client. It will accept either GET or POST methods or both

`/employee/look` —> input ID in form > return matching employee as json\
`/employee/all` — > return all employees as json\
`/employee/add` — > html form to add employee > return newly created employee as json\
`/employee/edit/<id>` — > fetch employee based on its id > popuate html form with it > return updated employee as json

`/menu/look`\
`/menu/all`\
`/menu/add`\
`/menu/edit/<id>`
