import datetime
import logging

from conf import config as cfg
from conf import utilities as util

# Data model representation, object designed to interact in first hand with DB for CRUD
# TODO: enhance with classes and attribute names with reflection
class ParentData:  # private - for inheritance purpose only
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    def __init__(self, db_wrap, id):
        # Each Obj knows the connection Wrapper and interact directly with it (therefore, main program totally ignores connection beside for opening and terminating)
        self.db = db_wrap  # SqliteWrapper obj
        self.id = id

    def fetch(self, qry, val=tuple()):
        self.db.gain_cursor()
        r = self.db.fetch_data(qry, val)
        self.db.close_cursor()
        logging.debug('DATA — Fetch::: %s\n\t--->%s', qry, val)
        return r

    def fetchone(self, qry, val=tuple()):
        self.db.gain_cursor()
        r = self.db.fetch_data_single(qry, val)
        self.db.close_cursor()
        logging.debug('DATA — Fetch::: %s\n\t--->%s', qry, val)
        return r

    def execute(self, qry, val):
        r = self.db.exec_data(qry, val)
        logging.debug('DATA — Exec::: Row ID(%s) %s\n\t--->%s', self.id, qry, val)
        return r

    def commit(self):
        self.db.commit_connection()
        logging.debug('DATA – Comm')
        return self


class Employee(ParentData):  # save() means INSERT, update means UPDATE

    def __init__(self, db, id=-1): # temporary placeholder ID to match legacy class
        super().__init__(db, id)
        self.f_name = ''
        self.l_name = ''
        self.email = ''

    def __str__(self):
        return type(self).__name__ + ' [' + str(self.id) + ']::: ' + self.f_name + ' ' + self.l_name

    def __dict__(self):
        """
        source for json rendering
        :return:
        """
        return {'id': self.id, 'first_name': self.f_name, 'last_name': self.l_name, 'email': self.email}

    def find(self, val=None):
        """
        Fetch single employee record from DB, handles IDs not present in DB, non static find so it can initialize the object
        :param val:
        :return:
        """
        self.id = val if val else self.id  # Ternary operator - if no params passed, then relying on obj init
        e = self.fetchone(cfg.QRY_EMPL_SLCT, (self.id,))
        if e is None: # sqlite 'fetchone()' + this test > allows the app to dig DB for potentially non-existing ID
            return False # return within to lighten code reading

        self.f_name = e[1] # DB is trusted for type
        self.l_name = e[2]
        self.email = e[3]
        return self

    @staticmethod
    def findall(db):
        """
        static makes it extra easy to use
        :param db:
        :return:
        """
        result = ParentData(db, -1).fetch(cfg.QRY_EMPL_SLCTA)
        result_dict = {}

        for idx, employee in enumerate(result):  # setting up the right keys (mainly for json consistency)
            result_dict[str(idx)] = {'id': employee[0], 'f_name': employee[1], 'l_name': employee[2], 'email': employee[3]}
            # str(index) to ease XML (dicttoxml) function
        return result_dict


    def save(self, params={}):
        """
        can be used with 'self' attributes or by passing a dict with additional needed params
        :param params:
        :return:
        """
        if params != {}: # dict gives more freedom for params passing
            self.f_name = params['f_name'] if 'f_name' in params else None # ternary operation + dict test
            self.l_name = params['l_name'] if 'l_name' in params else None
            self.email = params['email'] if 'email' in params else None
        self.id = self.execute(cfg.QRY_EMPL_INSRT, (self.f_name, self.l_name, self.email))

    def update(self):
        """
        always perform 'fetch/find' before updating. To to fully init obj attr, in case some aren't updated
        :return:
        """
        return self.execute(cfg.QRY_EMPL_UPDT, (self.f_name, self.l_name, self.email, self.id))

    def validate(self, params): # to call before performing before any DB operation against obj
        self.f_name = util.validate_string(params['f_name'] if 'f_name' in params else (util.validate_string(self.f_name)))
        self.l_name = util.validate_string(params['l_name'] if 'l_name' in params else (util.validate_string(self.l_name)))
        self.email = util.validate_string(params['email'] if 'email' in params else (util.validate_string(self.email)))

        if self.f_name is None or self.l_name is None: # these must be defined to satisfy DB constraint
            return False
        else:
            return self

class Menu(ParentData):

    def __init__(self, db, id=-1):
        super().__init__(db, id)
        self.descr = ''
        self.price = -1.0
        self.price_archive = -1.0 # the price stored in purchase detail,  initialized in purchase.find()

    def __str__(self):
        return type(self).__name__ + ' [' + str(self.id) + ']::: ' + self.descr + '@' + str(self.price)

    def __dict__(self):
        return {'id': self.id, 'descr': self.descr, 'price': self.price, 'price_archive': self.price_archive}

    def find(self, val=None):
        self.id = val if val else self.id
        m = self.fetchone(cfg.QRY_MENU_SLCT, (self.id,))
        if m is None:
            return False

        self.descr = m[1]
        self.price = float(m[2])
        return self

    @staticmethod
    def findall(db):
        result = ParentData(db, -1).fetch(cfg.QRY_MENU_SLCTA)
        result_dict = {}

        for idx, menu in enumerate(result):
            result_dict[str(idx)] = {'id': menu[0], 'descr': menu[1], 'price': menu[2]}

        return result_dict

    def save(self, params={}):
        if params != {}:
            self.descr = params['descr'] if 'descr' in params else None
            self.price = params['price'] if 'price' in params else None

        self.id = self.execute(cfg.QRY_MENU_INSRT, (self.descr, self.price))

    def update(self):
        return self.execute(cfg.QRY_MENU_UPDT, (self.descr, self.price, self.id))

    def validate(self, params):
        self.descr = util.validate_string(params['descr'] if 'descr' in params else (util.validate_string(self.descr)))
        self.price = util.validate_float(params['price'] if 'price' in params else (util.validate_float(self.price)))

        if self.descr is None or self.price is None:
            return False
        else:
            return self


class Purchase(ParentData):

    def __init__(self, db, id=-1):
        super().__init__(db, id)
        self.employee = None
        self.date = datetime.datetime.now().strftime(cfg.TIME_FORMAT)
        self.menu_list = []

    def __str__(self):
        return type(self).__name__ + ' [' + str(self.id) + ']::: ' + self.date + ' ' + str(self.employee)

    def __dict__(self):
        menu_list_dict = {}
        for idx, menu in enumerate(self.menu_list):
            menu_list_dict[str(idx)] = menu.__dict__()

        return {'id': self.id, 'date': self.date, 'employee': self.employee.__dict__(), 'menu_list': menu_list_dict}

    def addmenu(self, menu):
        self.menu_list.append(menu)
        return self

    def find(self, val=None):
        self.id = val if val else self.id
        p = self.fetchone(cfg.QRY_PURCH_SLCT, (self.id,))
        if p is None:
            return False

        self.date = p[1]
        # recovering employee from DB, passed ID isn't meat to be tested in the model
        self.employee = Employee(self.db).find(int(p[2]))
        pd_list = Purchase_Detail.filter_purchase(self.db, self.id)

        # recovering every menu object from DB and adding price_archive drom Purchase_Detail
        for pd in pd_list:
            curr_menu = int(pd_list[pd]['menu_id'])
            m = Menu(self.db).find(curr_menu)
            m.price_archive = float(pd_list[pd]['menu_price'])
            self.addmenu(m)

        return self

    @staticmethod
    def findall(db):
        result = ParentData(db, -1).fetch(cfg.QRY_PURCH_SLCTA)
        result_dict = {}

        for idx, purchase in enumerate(result):
            result_dict[str(idx)] = {'id': purchase[0], 'date': purchase[1], 'employee_id': purchase[2]}

        return result_dict

    def save(self, employee=None, date=None):
        self.employee = employee if employee else self.employee
        self.date = date if date else self.date

        self.id = self.execute(cfg.QRY_PURCH_INSRT, (self.date, self.employee.id))
        return self


class Purchase_Detail(ParentData):
    """
    This class should mainly be used through Purchase
    """
    def __init__(self, db, id=-1):
        super().__init__(db, id)
        self.purchase = None
        self.menu = None
        self.menu_price = -1.0

    def __str__(self):
        return type(self).__name__ + ' [' + str(self.id) + ']::: ' + str(self.menu.id) + ' ' + str(
            self.purchase.id) + ' ' + str(self.menu_price)

    def find(self, val=None):
        self.id = val if val else self.id
        pd = self.fetchone(cfg.QRY_PURCHDTL_SLCT, (self.id,))
        if pd is None:
            return False

        self.purchase = Purchase(self.db).find(int(pd[1]))
        self.menu = Menu(self.db).find(int(pd[2]))
        self.menu_price = float(pd[3])
        self.menu.price_archive = self.menu_price # ease obj manipulation from the menu object (printing older receipt)
        return self

    @staticmethod
    def findall(db):
        result = ParentData(db, -1).fetch(cfg.QRY_PURCHDTL_SLCTA)
        result_dict = {}

        for idx, purch_dtl in enumerate(result):
            result_dict[str(idx)] = {'id': str(purch_dtl[0]), 'purchase_id': str(purch_dtl[1]), 'menu_id': str(purch_dtl[2]), 'menu_price': str(purch_dtl[3])}

        return result_dict

    @staticmethod
    def filter_purchase(db, val):
        """
        recover all purchase_detail rows for a given purchase ID, no validation method since this class is only meant
        for internal use
        :param db:
        :param val:
        :return:
        """

        result = ParentData(db, -1).fetch(cfg.QRY_PURCHDTL_FINDA, (val,))
        result_dict = {}

        for purch_dtl in result:
            result_dict[str(purch_dtl[0])] = {'id': str(purch_dtl[0]), 'purchase_id': str(purch_dtl[1]), 'menu_id': str(purch_dtl[2]), 'menu_price': str(purch_dtl[3])}

        return result_dict

    def save(self, purchase=None, menu=None):
        self.purchase = purchase if purchase else self.purchase
        self.menu = menu if menu else self.menu

        self.id = self.execute(cfg.QRY_PURCHDTL_INSRT, (self.purchase.id, self.menu.id, self.menu.price))
        return self
