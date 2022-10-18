from datetime import datetime, timedelta

import psycopg2
import os
from pathlib import Path

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT'))


class DataBase:
    connection = psycopg2.connect(dbname=DATABASE_NAME, user=DATABASE_USERNAME,
                                       password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
    cursor = connection.cursor()

    @classmethod
    def get_user(cls, user_id):
        with cls.connection:
            cls.cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
            if cls.cursor.fetchone():
                return True
            return False

    @classmethod
    def get_user_lang(cls, user_id):
        with cls.connection:
            cls.cursor.execute('SELECT lang FROM users WHERE id=%s;', (user_id,))
            return cls.cursor.fetchone()

    @classmethod
    def change_lang(cls, user_id, lang):
        with cls.connection:
            cls.cursor.execute('UPDATE users SET lang=%s WHERE id=%s;', (lang, user_id))
            cls.connection.commit()

    @classmethod
    def register(cls, user_id, lang):
        with cls.connection:
            cls.cursor.execute('INSERT INTO users(id, lang) VALUES (%s, %s);', (user_id, lang))
            cls.connection.commit()


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

    def register(cls, user_id, lang):
        with cls.connection:
            cls.cursor.execute('INSERT INTO users(id, lang) VALUES (%s, %s)', (user_id, lang))
            cls.connection.commit()

    def tables(self, reserve_time):

        return self.check_time_reserve(1, reserve_time)

    def cabins(self, reserve_time):

        return self.check_time_reserve(2, reserve_time)

    def table_id(self, table, seating_category):
        with self.connection:
            self.cursor.execute(
                'SELECT id, min_capacity, max_capacity FROM tables WHERE name=%s and seating_category=%s;',
                (table, seating_category))
            return self.cursor.fetchall()

    def seating_category(self, id):
        with self.connection:
            self.cursor.execute('SELECT seating_name FROM seating_categories WHERE id=%s;', (id,))
            return self.cursor.fetchone()

    def check_time_reserve(self, category, time):
        with self.connection:
            free_tables = []
            busy_tables = []
            self.cursor.execute('SET TIME ZONE "Asia/Tashkent";')
            self.cursor.execute('SELECT id FROM booking;')
            for table in self.cursor.fetchall():
                self.cursor.execute('DELETE FROM booking WHERE end_at<now() and id=%s', (table,))
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
                            'SELECT name, min_capacity, max_capacity FROM tables WHERE seating_category=%s and id=%s ORDER BY id;',
                            (category, table,))
                        busy_tables.append(self.cursor.fetchone())
                self.cursor.execute(
                    'SELECT name, min_capacity, max_capacity FROM tables WHERE seating_category=%s ORDER BY id;',
                    (category,))
                result = self.cursor.fetchall()
                for tbl in result:
                    if tbl not in busy_tables:
                        free_tables.append(tbl)
            else:
                self.cursor.execute(
                    'SELECT name, min_capacity, max_capacity FROM tables WHERE seating_category=%s ORDER BY id;',
                    (category,))
                free_tables = self.cursor.fetchall()

            self.connection.commit()

            return free_tables

    def result(self):
        with self.connection:
            self.cursor.execute(
                'SELECT name FROM tables WHERE seating_category=1 ORDER BY id;')
            result = self.cursor.fetchall()
            return result
    # def check(self):
    #     self.cursor.execute('SELECT id FROM booking;')
    #     for table in self.cursor.fetchall():
    #         self.cursor.execute('DELETE FROM booking WHERE end_at<now() and id=%s', (table, ))
    #         self.connection.commit()


class Delivery(DataBase):
    def get_categories(self, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT name_%s FROM food_categories ORDER BY id;',
                (lang.replace("'", ''),))
            return self.cursor.fetchall()

    def get_categoryId(self, name, lang):
        with self.connection:
            try:
                self.cursor.execute(
                    'SELECT id FROM food_categories WHERE name_%s=%s;',
                    (lang, name))
                return self.cursor.fetchone()
            except:
                raise ValueError

    def get_dishes(self, cat_id, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT name_%s FROM foods WHERE category_id=%s ORDER BY id;',
                (lang, cat_id))
            return self.cursor.fetchall()

    def get_dish(self, name, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT id, name_%s, price, image FROM foods WHERE name_%s=%s',
                (lang, lang, name))
            return self.cursor.fetchone()

    def insert_toBasket(self, dish_id, qnt, price, user_id):
        with self.connection:
            self.cursor.execute('SET TIME ZONE "Asia/Tashkent"')
            self.cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
            if not self.cursor.fetchone():
                self.cursor.execute('INSERT INTO users (id) '
                                    'VALUES (%s);', (user_id,))

            self.cursor.execute(
                'SELECT * FROM basket WHERE user_id=%s and food_id=%s and ordered=false;', (user_id, dish_id,)
            )
            if self.cursor.fetchall():
                self.cursor.execute('UPDATE basket SET quantity = quantity+%s, price = price+%s, created_at=now() '
                                    'WHERE user_id=%s and food_id=%s and ordered=false;',
                                    (int(qnt), int(price), user_id, dish_id,))
            else:
                self.cursor.execute(
                    'INSERT INTO basket(food_id, quantity, price, user_id, created_at) VALUES (%s, %s, %s, %s, now());',
                    (dish_id, qnt, price, user_id))
            self.connection.commit()

    def show_basket(self, user_id, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT foods.name_%s, foods.price, basket.quantity, basket.price '
                'FROM basket '
                'JOIN foods ON basket.food_id=foods.id WHERE user_id=%s and ordered=false;', (lang, user_id))
            return self.cursor.fetchall()

    def foods_name(self, user_id, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT foods.name_%s '
                'FROM basket '
                'JOIN foods ON basket.food_id=foods.id WHERE user_id=%s and ordered=false;', (lang, user_id))
            return self.cursor.fetchall()

    def delete_good_from_basket(self, name, user_id, lang):
        with self.connection:
            self.cursor.execute(
                'DELETE FROM basket WHERE food_id in (SELECT id FROM foods WHERE name_%s=%s) and user_id=%s and ordered=false;',
                (lang, name, user_id))
            self.connection.commit()

    def checkout(self, user_id, address, phone_number):
        with self.connection:
            self.cursor.execute('SET TIME ZONE "Asia/Tashkent";')
            self.cursor.execute('UPDATE users SET phone_number=%s WHERE id=%s;', (phone_number, user_id))
            self.cursor.execute('SELECT price FROM basket WHERE user_id=%s and ordered=false;', (user_id,))
            total_price = 0
            for price in self.cursor.fetchall():
                total_price += price[0]
            self.cursor.execute(
                'INSERT INTO orders (baskets_id, address, total_price, created_at, user_id, phone_number) '
                'VALUES('
                'array[]::integer[], %s, %s, now(), %s, %s'
                ');', (address, total_price, user_id, phone_number))
            self.cursor.execute('select id from basket where user_id=%s and ordered=False;', (user_id,))
            for basket in self.cursor.fetchall():
                self.cursor.execute('UPDATE orders SET baskets_id=array_append(baskets_id, %s) '
                                    'where user_id=%s and ordered=FALSE ;',
                                    (basket[0], user_id))
            self.connection.commit()

    def order_id(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT id FROM orders WHERE user_id=%s', (user_id,))
            return self.cursor.fetchone()[0]

    def get_order(self, user_id, lang):
        with self.connection:
            self.cursor.execute(
                'SELECT foods.name_%s, foods.price, basket.quantity, basket.price '
                'FROM basket '
                'JOIN foods ON basket.food_id=foods.id WHERE user_id=%s and ordered=false;', (lang, user_id))
            return self.cursor.fetchall()

    def cancel_order(self, user_id):
        with self.connection:
            self.cursor.execute('DELETE FROM orders WHERE user_id=%s', (user_id,))
            self.cursor.execute('DELETE FROM basket WHERE user_id=%s', (user_id,))
            self.connection.commit()

    def accept_order(self, user_id):
        with self.connection:
            self.cursor.execute('UPDATE orders SET confirmed=True WHERE user_id=%s', (user_id,))
            self.cursor.execute('select id from basket where user_id=%s and ordered=False;', (user_id,))
            for basket in self.cursor.fetchall():
                self.cursor.execute('UPDATE basket SET ordered=TRUE where user_id=%s and id=%s;', (user_id, basket))
            self.connection.commit()


generalDB = DataBase()
bookingDB = Booking()
deliveryDB = Delivery()

# print(bookingDB.check())
# print(deliveryDB.test(275755142, 'qweqeqeqwe'))
# deliveryDB.insert_toBasket(21, 1, 105000, 275755142)
# deliveryDB.delete_good_from_basket('Каша с полезными продуктами', 275755142)
# print(deliveryDB.show_basket(275755142))
# deliveryDB.add_image_to_db()
# print(deliveryDB.foods_name(275755142))
# print(operations.result())
# print(bookingDB.check_time_reserve(2, datetime.strptime('2022-09-30 15:00', '%Y-%m-%d %H:%M')))
# print(bookingDB.start_booking(275755142, 2, '2022-09-30 15:00', '2022-09-30 18:00', '+998900336635', 'Ruslan', 2))
# operations.potencially_time(datetime.strptime('2022-09-29 15:00', '%Y-%m-%d %H:%M'))
# operations.tables(datetime.strptime('2022-10-05 18:00', '%Y-%m-%d %H:%M'))
