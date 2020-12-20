import sqlite3 as sqlt
import logging


class SqliteWrapper:  # Abstracting DB
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    def get_decorator(errors=(Exception,), default_value=False):
        def decorator(func):
            def new_func(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.getLogger(__name__).error(e)
                    return default_value

            return new_func

        return decorator

    handle_sqlite_exception = get_decorator((KeyError, NameError), False)

    def __init__(self, path):
        # TODO: Test Path
        self.path = path
        self.database = None
        self.cursor = None

    def __str__(self):
        return 'Path: ' + self.path + ' || Connection: ' + str(self.database)

    ###########################__DATABASE__#############################################################################
    @handle_sqlite_exception
    def initiate_connection(self):
        connection = sqlt.connect(self.path)
        self.database = connection if connection else None
        return self.database

    @handle_sqlite_exception
    def terminate_connection(self):
        self.database.close()

    @handle_sqlite_exception
    def commit_connection(self):
        self.database.commit()

    ###########################__CURSOR__###############################################################################
    @handle_sqlite_exception
    def gain_cursor(self):
        self.cursor = self.database.cursor()

    @handle_sqlite_exception
    def close_cursor(self):
        self.cursor.close()
        self.cursor = None

    @handle_sqlite_exception
    def execute_cursor(self, query, value):  # private
        return self.cursor.execute(query, value)

    ###########################__DATA__#################################################################################
    def exec_data(self, query, value):
        self.execute_cursor(query, value)
        return self.cursor.lastrowid # in case of UPDATE rowid = 0

    def fetch_data(self, query, value):
        return self.execute_cursor(query, value).fetchall()

    def fetch_data_single(self, query, value):
        return self.execute_cursor(query, value).fetchone()
    ####################################################################################################################

