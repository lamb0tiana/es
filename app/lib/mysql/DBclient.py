import os
import mysql.connector
from dotenv import load_dotenv
from lib.tools import generate_matching_query, extract_insertable_field_data, build_insert_query

load_dotenv()

class DBclient:

    def __init__(self, db: str):
        try:
            self.connexionDB = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=db
            )
            if self.connexionDB.is_connected():
                self.cursor = self.connexionDB.cursor(dictionary=True)
                print("Connected to the database successfully!")
            else:
                print("Failed to connect to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connexionDB = None

    def close_connection(self):
        if self.connexionDB and self.connexionDB.is_connected():
            self.connexionDB.close()

    def match_string(self, criteria: str , id: str):
        if self.connexionDB and self.connexionDB.is_connected():
            try:
                cursor = self.connexionDB.cursor(dictionary=True)
                query = generate_matching_query(criteria)
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error Code: {err.errno}")
                print(f"SQLSTATE: {err.sqlstate}")
                print(f"Error Message: {err.msg}")
                return []
        else:
            print("No active database connection.")
            return []

    def create_contact(self, fields: list):

        if self.connexionDB and self.connexionDB.is_connected():
            try:
                row_data = extract_insertable_field_data(fields)
                query = build_insert_query(row_data)
                self.cursor.execute(query)
                self.connexionDB.commit()
                return self.cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Error Code: {err.errno}")
                print(f"SQLSTATE: {err.sqlstate}")
                print(f"Error Message: {err.msg}")
                return None

        else:
            print("No active database connection.")
            return None