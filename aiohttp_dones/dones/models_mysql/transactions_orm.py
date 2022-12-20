import enum
import time
from datetime import datetime
import mysql.connector.pooling
from flask import current_app as app

connection_pool = None


class Transactions:
    @staticmethod
    def get_all_transactions():
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM tbl_transactions ")
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_transaction_by_id(transaction_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE id='%(id)s'"
        cursor.execute(query, {'id': transaction_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def get_transaction_by_asset_id(asset_id):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM tbl_transactions WHERE asset_id=%(asset_id)s"
        cursor.execute(query, {'asset_id': asset_id})
        row = cursor.fetchone()
        cnx.close()
        return row

    @staticmethod
    def insert_new_transaction(account_id, asset_id, amount, create_datetime, transaction_type, status, asset_price_at_transaction_time, description):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        add_transaction = ("INSERT INTO `tbl_transactions` (`account_id`, `asset_id`, `amount`, `create_datetime`, `transaction_type`, `status`, `asset_price_at_transaction_time`, `description`) VALUES" +
                           "( %(account_id)s, %(asset_id)s, %(amount)s, %(create_datetime)s, %(transaction_type)s, %(status)s, %(asset_price_at_transaction_time)s, %(description)s)")
        data_transaction = {
            'account_id': account_id,
            'asset_id': asset_id,
            'amount': amount,
            'create_datetime': create_datetime,
            'transaction_type': transaction_type.value,
            'status': status.value,
            'asset_price_at_transaction_time': asset_price_at_transaction_time,
            'description': description,
        }
        cursor.execute(add_transaction, data_transaction)
        inserted_record_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return inserted_record_id

    @staticmethod
    def update_transaction(id, account_id=None, asset_id=None, amount=None, create_datetime=None, transaction_type=None, status=None, asset_price_at_transaction_time=None, description=None):
        global connection_pool
        if connection_pool == None:
            connection_pool = app.config['mysql_connection_pool']
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        update_string = ''
        if account_id:
            update_string += f'account_id = %(account_id)s,'
        if asset_id:
            update_string += f'asset_id=%(asset_id)s,'
        if amount:
            update_string += f'amount=%(amount)s,'
        if create_datetime:
            update_string += f'create_datetime=%(create_datetime)s,'
        if transaction_type:
            update_string += f'transaction_type=%(transaction_type)s,'
        if status:
            update_string += f'status=%(status)s,'
        if asset_price_at_transaction_time:
            update_string += f'asset_price_at_transaction_time=%(asset_price_at_transaction_time)s,'
        if description:
            update_string += f'description=%(description)s,'
        update_string = update_string.rstrip(',')
        add_transaction = f"UPDATE tbl_transactions SET {update_string} WHERE id='{id}'"
        data_transaction = {
            'account_id': account_id,
            'asset_id': asset_id,
            'amount': amount,
            'create_datetime': create_datetime,
            'transaction_type': transaction_type,
            'status': status,
            'asset_price_at_transaction_time': asset_price_at_transaction_time,
            'description': description,
        }
        cursor.execute(add_transaction, data_transaction)
        cnx.commit()
        cnx.close()
        return True

    class Status(enum.Enum):
        Unknown = enum.auto()
        successful = enum.auto()
        failed = enum.auto()
        pending = enum.auto()
        expired = enum.auto()
        queued = enum.auto()
        canceling = enum.auto()
        canceled = enum.auto()

    class Types(enum.Enum):
        ipg_cash_deposit = enum.auto()
        admin_cash_deposit = enum.auto()
        gift_cash_deposit = enum.auto()
        cash_withdrawal = enum.auto()
        buy_token = enum.auto()
        sell_token = enum.auto()
        token_withdrawal = enum.auto()


def transactions_orm_functions_test():
    import random
    i = random.randint(1, 1000)
    last_id = Transactions.insert_new_transaction(i, i, i, time.time(
    ), Transactions.Types.buy_token, Transactions.Status.pending, 0, f'{i*11}')
    update = Transactions.update_transaction(last_id, account_id=i*2)
    last_transaction = Transactions.get_transaction_by_id(last_id)
    print(last_transaction)
    print('-' * 80)
    all_transactions = Transactions.get_all_transactions()
    print(all_transactions)


if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        user="root", password="", database='goldis', use_pure=False, pool_name="my_pool", pool_size=32, buffered=True)
    transactions_orm_functions_test()
    print('Everything is alright!')