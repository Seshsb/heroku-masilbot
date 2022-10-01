from datetime import datetime, timedelta

import psycopg2
import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT'))

connection = psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USERNAME,
                              password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
cursor = connection.cursor()


class DataBaseOperations:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USERNAME,
                              password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
        self.cursor = self.connection.cursor()

    def user_exist(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))
            result = self.cursor.fetchall()
            return bool(len(result))

    def start_booking(self, user_id, table_id, start_at, end_at, phone_number, name, people):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
            if not self.cursor.fetchone():
                self.cursor.execute('INSERT INTO users (id, first_name, phone_number) '
                                    'VALUES (%s, %s, %s);', (user_id, name, phone_number))
            else:
                self.cursor.execute('UPDATE users SET first_name=%s, phone_number=%s WHERE id=%s;', (name, phone_number,
                                                                                                     user_id))
            self.cursor.execute('INSERT INTO booking (tbl_id, start_at, end_at, user_id, people) '
                                'VALUES (%s, %s, %s, %s, %s);', (table_id, start_at, end_at, user_id, people))
            self.connection.commit()

    def tables(self, reserve_time):
        with self.connection:
            self.cursor.execute('SELECT start_at, end_at, tbl_id FROM booking WHERE date(start_at)=%s;',
                                (reserve_time.date(), ))
            if self.cursor.fetchall():
                self.cursor.execute('SELECT start_at, end_at, tbl_id FROM booking WHERE date(start_at)=%s;',
                                    (reserve_time.date(),))
                for start, end, table in self.cursor.fetchall():
                    range_hours = []
                    if reserve_time.date() == start.date():
                        for time_hours in range(start.hour-2, end.hour+4):
                            range_hours.append(time_hours)
                    if reserve_time.hour not in range_hours:
                        self.cursor.execute(
                            'SELECT name FROM tables WHERE seating_category=1 and is_occupied=false ORDER BY id;')
                        return self.cursor.fetchall()
                    else:
                        self.cursor.execute(
                            'SELECT name FROM tables WHERE seating_category=1 and id!=%s ORDER BY id;', (table, ))
                        return self.cursor.fetchall()
            else:
                self.cursor.execute(
                    'SELECT name FROM tables WHERE seating_category=1 and is_occupied=false ORDER BY id;')
                print(self.cursor.fetchall())

    def cabins(self):
        with self.connection:
            self.cursor.execute('SELECT name FROM tables WHERE seating_category=2 and is_occupied=false ORDER BY id;')
            return self.cursor.fetchall()

    def table_id(self, table, seating_category):
        with self.connection:
            self.cursor.execute('SELECT id FROM tables WHERE name=%s and seating_category=%s;', (table, seating_category))
            return self.cursor.fetchone()

    def seating_category(self, id):
        with self.connection:
            self.cursor.execute('SELECT seating_name FROM seating_categories WHERE id=%s;', (id, ))
            return self.cursor.fetchone()

    # def potencially_time(self, reserve_time):
    #     with self.connection:
    #         self.cursor.execute('SELECT start_at, end_at, tbl_id FROM booking WHERE date(start_at)=%s;', (reserve_time.date(), ))
    #         print(self.cursor.fetchall())

    # def check_book(self, tbl_id, date_time):
    #     with self.connection:
    #         self.cursor.execute('SELECT start_at, end_at FROM booking WHERE tbl_id=%s;', (tbl_id, ))
    #         for start, end in self.cursor.fetchall():
    #             self.cursor.execute('SELECT DATE_PART(month, %s;', (start, ))
    #             print(self.cursor.fetchall())


operations = DataBaseOperations()
# # operations.start_booking(275755142, 2, '2022-09-30 15:00', '2022-09-30 18:00', '+998900336635', 'Ruslan', 2)
# operations.potencially_time(datetime.strptime('2022-09-29 15:00', '%Y-%m-%d %H:%M'))
# operations.tables(datetime.strptime('2022-10-02 12:00', '%Y-%m-%d %H:%M'))