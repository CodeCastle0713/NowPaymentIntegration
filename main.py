import time
import requests
import os
from dotenv import load_dotenv
from sqlite import create_payment_table, insert_payment

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODE = os.getenv("MODE")
CASE = os.getenv("CASE")

def create_payment(amount, price_currency, pay_currency, order_id):
    urlPayment = f"{BASE_URL}/payment"

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "price_amount": amount,
        "price_currency": price_currency, 
        "pay_currency": pay_currency,     
        "order_id": order_id,
        "success_url": "https://wordpress.com",
        "cancel_url": "https://wordpress.com",
    }
    
    if(MODE == "test"):
        payload['case'] = CASE

    responsePayment = requests.post(urlPayment, json=payload, headers=headers)

    print(f"Payment: {responsePayment.json()}")

    if responsePayment.status_code == 201:
        payment_data = responsePayment.json()
        return payment_data["payment_id"]
    else:
        raise Exception(f"Error: {responsePayment.status_code} - {responsePayment.text}")

def get_payment_status(payment_id):
    url = f"{BASE_URL}/payment/{payment_id}"
    print("URL:", url)
    headers = {
        'x-api-key': API_KEY
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def poll_for_payment_status(telegram_id, amount, payment_id, check_interval):
    while True:
        try:
            payment_info = get_payment_status(payment_id)
            payment_status = payment_info.get("payment_status")
            print(f"Payment Status: {payment_status}")

            if payment_status == "finished":
                print("Payment completed successfully!")
                insert_payment(telegram_id, amount, payment_status)
                break
            elif payment_status == "failed":
                print("Payment failed!")
                insert_payment(telegram_id, amount, payment_status)
                break
            else:
                print("Payment is still in progress...")
            
            time.sleep(check_interval)

        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    try:
        create_payment_table()
        payment_id = create_payment(
            amount=150.0,
            price_currency="usd",
            pay_currency="btc",
            order_id="123456789",
        )
        
        poll_for_payment_status("12312312323", 150, payment_id, check_interval=3)
        
    except Exception as e:
        print(e)
