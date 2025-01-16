import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = "payment_database.db" 

def connect_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    return cursor, connection

def create_payment_table():
    connection = None
    cursor = None
    try:
        cursor, connection = connect_db()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS payment_history (
                telegram_id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount DECIMAL(15, 2),
                payment_status VARCHAR(50)
            );
        '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table creating/connection successfully in SQLite")

    except sqlite3.Error as error:
        print("Error while connecting to SQLite:", error)
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("SQLite connection is closed")

def insert_payment(telegram_id, amount, status):
    connection = None
    cursor = None
    try:
        cursor, connection = connect_db()

        insert_query = '''
            INSERT INTO payment_history 
            (telegram_id, amount, payment_status)
            VALUES (?, ?, ?)
        '''
        
        record_to_insert = (
            telegram_id,
            amount,
            status,
        )

        cursor.execute(insert_query, record_to_insert)
        inserted_id = cursor.lastrowid 
        connection.commit()
        print(f"Payment record inserted successfully. ID: {inserted_id}")
        return inserted_id

    except sqlite3.Error as error:
        print("Error while inserting data:", error)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()