import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def connect_db():
    connection = psycopg2.connect(
        user = DATABASE_USER,
        password = DATABASE_PASSWORD,
        host = DATABASE_HOST,
        port = DATABASE_PORT,
        database = DATABASE_NAME
    )
    cursor = connection.cursor()
    return cursor, connection

def create_payment_table():
    connection = None
    cursor = None
    try:
        cursor, connection = connect_db()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS payment_history (
                telegram_id SERIAL PRIMARY KEY,
                amount DECIMAL(15, 2),
                payment_status VARCHAR(50)
            );
        '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table creating/connection successfully in PostgreSQL")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")

def insert_payment(telegram_id, amount, status):
    connection = None
    cursor = None
    try:
        cursor, connection = connect_db() 

        insert_query = '''
            INSERT INTO payment_history 
            (telegram_id, amount, payment_status)
            VALUES (%s, %s, %s)
            RETURNING telegram_id;
        '''
        
        record_to_insert = (
            telegram_id,
            amount,
            status,
        )

        cursor.execute(insert_query, record_to_insert)
        inserted_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Payment record inserted successfully. ID: {inserted_id}")
        return inserted_id

    except (Exception, Error) as error:
        print("Error while inserting data:", error)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()