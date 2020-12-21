DB_DIR = 'data/'
DB_NAME = 'meals.db'

TIME_FORMAT = "%d-%m-%Y %H:%M:%S"

ERROR_MSG_PARAM = 'Wrong or missing input'
ERROR_MSG_DB = 'Error reading database (possibly wrong ID)'

HEADER_JSON = {'Content-Type': 'application/json; charset=utf-8'}
HEADER_XML = {'Content-Type': 'application/xml; charset=utf-8'}
SENDFILE_PDF = 'application/pdf'

COMPANY_ADDRESS = {'name': 'ABC inc.', 'street': 'Waterloo street', 'number': 1, 'city': 'Brussels', 'zip': 1000, 'vat_number': 'BE 0123 456 789', 'vat': 6.0}
DFLT_FILENAME = 'receipt_{0}.pdf'

PDF_LINE_HEIGHT = 8

# GLOBAL CONST
QRY_EMPL_SLCT = 'SELECT id, first_name,family_name,email_address FROM employee WHERE id=?'
QRY_EMPL_SLCTA = 'SELECT * FROM employee'
QRY_EMPL_INSRT = 'INSERT INTO employee(first_name,family_name,email_address) VALUES (?,?,?)'
QRY_EMPL_UPDT = 'UPDATE employee SET first_name=?, family_name=?, email_address=? WHERE id=?'

QRY_MENU_SLCT = 'SELECT id, description, price FROM menu WHERE id=?'
QRY_MENU_SLCTA = 'SELECT * FROM menu'
QRY_MENU_INSRT = 'INSERT INTO menu(description,price) VALUES (?,?)'
QRY_MENU_UPDT = 'UPDATE menu SET description=?, price=? WHERE id=?'

QRY_PURCH_SLCT = 'SELECT id, date, employee_id FROM purchase WHERE id=?'
QRY_PURCH_SLCTA = 'SELECT * FROM purchase'
QRY_PURCH_INSRT = 'INSERT INTO purchase(date,employee_id) VALUES (?,?)'

QRY_PURCHDTL_SLCT = 'SELECT id, purchase_id, menu_id, menu_price FROM purchase_detail WHERE id=?'
QRY_PURCHDTL_SLCTA = 'SELECT * FROM purchase_detail'
QRY_PURCHDTL_FINDA = 'SELECT * FROM purchase_detail WHERE purchase_id=?'
QRY_PURCHDTL_INSRT = 'INSERT INTO purchase_detail(purchase_id,menu_id,menu_price) VALUES (?,?,?)'
# GLOBAL CONST

RECEIPT_FILE_MSG = '''<h1>Serving pdf receipt</h1>'''

FORM_EMPL_VIEW = '''<h1>View Employee by ID</h1>
                <form method="POST">
                    <input type="text" name="id" placeholder="Employee id"><br>
                    <input type="submit" value="Submit"><br>
                </form>'''

FORM_EMPL_ADD = '''<h1>Add Employee</h1>
                <form method="POST">
                    <input type="text" name="f_name" placeholder="First name..."><br>
                    <input type="text" name="l_name" placeholder="Last name..."><br>
                    <input type="text" name="email" placeholder="Email..."><br>
                    <input type="submit" value="Submit"><br>
                </form>'''

FORM_EMPL_EDIT = '''xxx''' #see 'template' folder

FORM_MENU_VIEW = '''<h1>View Menu by ID</h1>
                <form method="POST">
                    <input type="number" name="id" placeholder="Menu id"><br>
                    <input type="submit" value="Submit"><br>
                </form>'''

FORM_MENU_ADD = '''<h1>Add Menu</h1>
                <form method="POST">
                    <input type="text" name="descr" placeholder="Description..."><br>
                    <input type="text" name="price" placeholder="Price..."><br>
                    <input type="submit" value="Submit"><br>
                </form>'''

FORM_MENU_EDIT = '''xxx''' #see 'template' folder

FORM_PURCH_ADD = '''<h1>Record Purchase</h1>
                <form method="POST">
                    <input type="text" name="empl_id" placeholder="Employee id..."><br>
                    <input type="text" name="menu_id_list" placeholder="Menu id... ex: 2,10,3"><br>
                    <input type="submit" value="Submit"><br>
                </form>'''
