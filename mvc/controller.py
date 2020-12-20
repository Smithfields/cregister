from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from mvc.model import *
from src.wrapper import *

from conf import config as cfg

from html import escape as htescape
import io


DB_PATH = cfg.DB_DIR + cfg.DB_NAME
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


########################################################################################################################
# EMPLOYEE SECTION #####################################################################################################
########################################################################################################################
def find_employee(id):
    logging.info('Controller — Employee::: FIND')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    e = Employee(ds, id).find()
    ds.terminate_connection()
    return e


def find_all_employee():
    logging.info('Controller — Employee::: FIND ALL')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    e_all = Employee.findall(ds)
    ds.terminate_connection()
    return e_all


def add_employee(data):
    logging.info('Controller — Employee::: ADD')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()

    e = Employee(ds)

    if not e.validate(
            {'f_name': htescape(data['f_name']), 'l_name': htescape(data['l_name']), 'email': htescape(data['email'])}):
        return False

    ds.gain_cursor()
    e.save()
    ds.commit_connection()
    ds.close_cursor()
    ds.terminate_connection()
    return e


def update_employee(id, data):
    logging.info('Controller — Employee::: UPDATE')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    e = Employee(ds, id).find()

    if not e.validate(
        {'f_name': htescape(data['f_name']), 'l_name': htescape(data['l_name']), 'email': htescape(data['email'])}):
        return False

    ds.gain_cursor()
    e.update()
    ds.commit_connection()
    ds.close_cursor()
    ds.terminate_connection()
    return e

########################################################################################################################
# MENU SECTION #########################################################################################################
########################################################################################################################
def find_menu(id):
    logging.info('Controller — Menu::: FIND')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    m = Menu(ds, id).find()
    ds.terminate_connection()
    return m


def find_all_menu():
    logging.info('Controller — Menu::: FIND ALL')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    m_all = Menu.findall(ds)
    ds.terminate_connection()
    return m_all


def add_menu(data):
    logging.info('Controller — Menu::: ADD')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()

    m = Menu(ds)

    if not m.validate({'descr': htescape(data['descr']), 'price': htescape(data['price'])}):
        return False

    ds.gain_cursor()
    m.save()
    ds.commit_connection()
    ds.close_cursor()
    ds.terminate_connection()
    return m


def update_menu(id, data):
    logging.info('Controller — Menu::: UPDATE')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    m = Menu(ds, id).find()

    if not m.validate({'descr': htescape(data['descr']), 'price': data['price']}):
        return False

    ds.gain_cursor()
    m.update()
    ds.commit_connection()
    ds.close_cursor()
    ds.terminate_connection()
    return m

########################################################################################################################
# PURCHASE SECTION #####################################################################################################
########################################################################################################################
def find_purchase(id):
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    p = Purchase(ds).find(id)
    ds.terminate_connection()
    return p

def initiate_purchase():
    logging.info('Controller — Purchase::: INIT PURCH')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    p = Purchase(ds)
    ds.terminate_connection()
    return p


def do_total_purchase(p, e):
    """
    save existing purchase and save all underlying purchase_detail
    :param p:
    :param e:
    :return:
    """
    logging.info('Controller — Purchase::: DO PURCH')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    ds.gain_cursor() # updating its connection obj since it got created (and closed) in another instance
    p.db = ds
    p.save(employee=e) # TODO: no need for employee param?

    for m in p.menu_list:
        pd = Purchase_Detail(ds)
        pd.save(purchase=p, menu=m)

    ds.commit_connection()
    ds.close_cursor()
    ds.terminate_connection()
    return p

########################################################################################################################
# RECEIPT SECTION ######################################################################################################
########################################################################################################################
def prepare_receipt_data(id):
    logging.info('Controller — RECEIPT::: INIT RECEIPT')
    ds = SqliteWrapper(DB_PATH)
    ds.initiate_connection()
    p = Purchase(ds).find(id)

    if not p:
        return False

    table = []

    table.append(cfg.COMPANY_ADDRESS['name'])
    table.append(cfg.COMPANY_ADDRESS['street'] + ', ' + str(cfg.COMPANY_ADDRESS['number']))
    table.append(str(cfg.COMPANY_ADDRESS['zip']) + ' ' + cfg.COMPANY_ADDRESS['city'])
    table.append('')
    table.append('Purchase number: ' + str(p.id))
    table.append('Employee: ' + str(p.employee.f_name) + ' ' + str(p.employee.l_name))
    table.append('')

    total = 0.0
    for menu in p.menu_list:
        table.append('{0:4}: {1:20}{2:5}€'.format('Menu', menu.descr, str(menu.price_archive)))
        total += menu.price_archive

    table.append('----------------------------------------------------------')

    vatval = (total * cfg.COMPANY_ADDRESS['vat']) / 100
    vattotal = vatval + total

    table.append('{0:<10}{1:>17}{2:>11}{3:>17}'.format('', 'excl. VAT', 'VAT', 'incl. VAT'))
    table.append('{0:<10}{1:>12}{2:>11}{3:>12}'.format('VAT ' + str(cfg.COMPANY_ADDRESS['vat']) + '%', str(total), str(vatval), str(vattotal)))
    table.append('----------------------------------------------------------')
    table.append('{0:<15}{1:>40}€'.format('TOTAL', str(vattotal)))
    table.append('Date: ' + p.date)
    table.append('VAT Number: ' + cfg.COMPANY_ADDRESS['vat_number'])

    return table


def make_receipt_cnsl(receipt_array):
    logging.info('Controller — RECEIPT::: PRINT RECEIPT CONSOLE')
    for line in receipt_array:
        print(line)
        return True


def make_receipt_pdf(receipt_array):
    logging.info('Controller — RECEIPT::: PRINT RECEIPT PDF')
    #storing canvas in a buffer to return it as a file
    buffer = io.BytesIO()
    c = Canvas(buffer, pagesize=(88*mm, 200*mm))
    pdfmetrics.registerFont(TTFont('Courier New', 'Courier New.ttf')) # monospaced font
    c.setFont('Courier New', 11)
    #c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText()
    textobject.setTextOrigin(10, 540)
    for line in receipt_array:
        textobject.textLine(line)
        textobject.moveCursor(0, 3)

    c.drawText(textobject)

    c.showPage()
    c.save()
    #reset the buffer cusor's position to 0
    buffer.seek(io.SEEK_SET)
    return buffer
