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


class DataBase:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USERNAME,
                                           password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
        self.cursor = self.connection.cursor()


class Booking(DataBase):
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

        return self.check_time_reserve(1, reserve_time)

    def cabins(self, reserve_time):

        return self.check_time_reserve(2, reserve_time)

    def table_id(self, table, seating_category):
        with self.connection:
            self.cursor.execute('SELECT id FROM tables WHERE name=%s and seating_category=%s;',
                                (table, seating_category))
            return self.cursor.fetchone()

    def seating_category(self, id):
        with self.connection:
            self.cursor.execute('SELECT seating_name FROM seating_categories WHERE id=%s;', (id,))
            return self.cursor.fetchone()

    def check_time_reserve(self, category, time):
        with self.connection:
            free_tables = []
            busy_tables = []
            self.cursor.execute('SELECT start_at, end_at, tbl_id FROM booking WHERE date(start_at)=%s;',
                                (time.date(),))
            if self.cursor.fetchall():
                self.cursor.execute('SELECT start_at, end_at, tbl_id FROM booking WHERE date(start_at)=%s;',
                                    (time.date(),))
                for start, end, table in self.cursor.fetchall():
                    range_hours = []
                    if time.date() == start.date():
                        for time_hours in range(start.hour - 2, end.hour + 1):
                            range_hours.append(time_hours)
                    if time.hour in range_hours:
                        self.cursor.execute(
                            'SELECT name FROM tables WHERE seating_category=%s and id=%s ORDER BY id;',
                            (category, table,))
                        busy_tables.append(self.cursor.fetchone())
                self.cursor.execute(
                    'SELECT name FROM tables WHERE seating_category=%s ORDER BY id;', (category,))
                result = self.cursor.fetchall()
                for tbl in result:
                    if tbl not in busy_tables:
                        free_tables.append(tbl)
            else:
                self.cursor.execute(
                    'SELECT name FROM tables WHERE seating_category=%s ORDER BY id;', (category,))
                free_tables = self.cursor.fetchall()

            return free_tables

    def result(self):
        with self.connection:
            self.cursor.execute(
                'SELECT name FROM tables WHERE seating_category=1 ORDER BY id;')
            result = self.cursor.fetchall()
            return result


class Delivery(DataBase):
    def get_categories(self):
        with self.connection:
            self.cursor.execute(
                'SELECT name_rus, name_kor FROM food_categories;'
            )
            return self.cursor.fetchall()

    def get_categoryId(self, name):
        with self.connection:
            try:
                self.cursor.execute(
                    'SELECT id FROM food_categories WHERE name_rus=%s;',
                    (name,))
                return self.cursor.fetchone()
            except:
                raise ValueError

    def get_dishes(self, cat_id):
        with self.connection:
            self.cursor.execute(
                'SELECT name_rus, name_kor FROM foods WHERE category_id=%s;',
                (cat_id,))
            return self.cursor.fetchall()

    def get_dish(self, name):
        with self.connection:
            self.cursor.execute(
                'SELECT id, name_rus, price FROM foods WHERE name_rus=%s',
                (name, ))
            return self.cursor.fetchone()

    def insert_toBasket(self, dish_id, qnt, price, user_id):
        with self.connection:
            self.cursor.execute(
                'INSERT INTO basket(food_id, quantity, price, user_id) VALUES (%s, %s, %s, %s);',
                (dish_id, qnt, price, user_id))
            self.connection.commit()

bookingDB = Booking()
deliveryDB = Delivery()
print(deliveryDB.get_dish('Рис с мясом и овощами в соусе '))
# print(operations.result())
# # operations.start_booking(275755142, 2, '2022-09-30 15:00', '2022-09-30 18:00', '+998900336635', 'Ruslan', 2)
# operations.potencially_time(datetime.strptime('2022-09-29 15:00', '%Y-%m-%d %H:%M'))
# operations.tables(datetime.strptime('2022-10-05 18:00', '%Y-%m-%d %H:%M'))
