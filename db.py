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

    def start_booking(self, user_id, table_id, time_at, phone_number, name):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
            if not self.cursor.fetchall():
                self.cursor.execute('INSERT INTO users (id, first_name, phone_number) '
                                    'VALUES (%s, %s, %s);', (user_id, name, phone_number))
            else:
                self.cursor.execute('UPDATE users SET first_name=%s, phone_number=%s WHERE id=%s;', (name, phone_number, user_id))
            self.cursor.execute('INSERT INTO booking (tbl_id, start_at, user_id) '
                                'VALUES (%s, %s, %s);', (table_id, time_at, user_id))
            self.connection.commit()

    def tables(self):
        with self.connection:
            self.cursor.execute('SELECT id FROM tables WHERE seating_category=1;')
            return self.cursor.fetchall()

operations = DataBaseOperations()
print(operations.tables())
