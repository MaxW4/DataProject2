sudo pip install requests

import asyncio
import requests
import sqlite3
from datetime import datetime

async def fetch_and_store_data():
    response = requests.get('https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi')
    if response.status_code == 200:
        data = response.json()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS api_data (
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            field1 TEXT,
                            field2 TEXT,
                            ...
                            )''')
        cursor.execute('''INSERT INTO api_data (timestamp, field1, field2, ...) VALUES (?, ?, ?, ...)''', 
                        (datetime.now(), data['field1'], data['field2'], ...))
        connection.commit()
        connection.close()

async def main():
    for i in range(60):
        print(f"Fetching data at {datetime.now()}")  
        await fetch_and_store_data()
        await asyncio.sleep(60)  # Wait for 60 seconds

# Run the event loop
asyncio.run(main())
