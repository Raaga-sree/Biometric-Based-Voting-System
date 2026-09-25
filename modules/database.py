import os
import mysql.connector
from mysql.connector import Error

print("Loaded database from:", __file__)


class Database:
    def __init__(
        self,
        host=None,
        database=None,
        user=None,
        password=None,
        port=None
    ):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.database = database or os.getenv("DB_NAME", "biometric_voting")
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password or os.getenv("DB_PASSWORD")
        self.port = int(port or os.getenv("DB_PORT", "3306"))

        self.conn = None
        self.connect()  # auto-connect on start

    # ---------- CONNECTION ----------
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )

            return self.conn.is_connected()

        except Error as e:
            print("DB Error:", e)
            self.conn = None
            return False

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def get_cursor(self, dictionary=False):
        if not self.conn or not self.conn.is_connected():
            self.connect()

        return self.conn.cursor(dictionary=dictionary)

    # ---------- USER ----------
    def delete_user(self, voter_id):
        cursor = self.get_cursor()

        cursor.execute(
            "DELETE FROM users WHERE voter_id=%s",
            (voter_id,)
        )

        self.conn.commit()
        cursor.close()

    def insert_user(self, name, age, voter_id, password_hash, pin_hash):
        cursor = self.get_cursor()

        query = """
        INSERT INTO users (name, age, voter_id, password_hash, pin_hash, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, age, voter_id, password_hash, pin_hash, 'user')
        )

        self.conn.commit()
        cursor.close()

        return voter_id

    def get_user_by_voter_id(self, voter_id):
        cursor = self.get_cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE voter_id = %s",
            (voter_id,)
        )

        user = cursor.fetchone()
        cursor.close()

        return user

    # ---------- ELECTION ----------
    def insert_election(self, name, start_date, end_date):
        cursor = self.get_cursor()

        query = """
        INSERT INTO elections (name, start_date, end_date)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, start_date, end_date))

        self.conn.commit()
        election_id = cursor.lastrowid
        cursor.close()

        return election_id

    def get_all_elections(self):
        cursor = self.get_cursor(dictionary=True)

        cursor.execute("SELECT * FROM elections")

        elections = cursor.fetchall()
        cursor.close()

        return elections