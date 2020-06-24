import psycopg2

from config import DATABASE, USER, PASSWORD, HOST, PORT

class DbLighter:

    def __init__(self):
        self.connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscriptions WHERE status = {status}")
            return self.cursor.fetchall()

    def subscriber_exist(self, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscriptions WHERE user_id = '{user_id}'")
            result = self.cursor.fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            self.cursor.execute(f"INSERT INTO subscriptions (user_id, status) VALUES ('{user_id}', {status})")

    def update_subscription(self, user_id, status):
        with self.connection:
            self.cursor.execute(f"UPDATE subscriptions SET status = {status} WHERE user_id = '{user_id}'")

    def close(self):
        self.connection.close
