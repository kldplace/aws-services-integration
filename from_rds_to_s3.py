import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# --- DATABASE CREDENTIALS ---
host= os.getenv('DB_HOST')
database= os.getenv('DB_DATABASE')
user= os.getenv('DB_USER')
password= os.getenv('DB_PASSWORD')

# --- DATABASE CONNECTION ---
try:
    connection = mysql.connector.connect(
        host= host,
        database= database,
        user= user,
        password= password
        )
    if connection.is_connected():
        print("Connected to MySQL Server succeeded")
except Exception:
    print("Connection to MySQL Server is failed")

# SET MySQL CURSOR
cursor = connection.cursor()

# --- MY QUERIES ---
# The [show_id] of Saudi arabia movies in Netflix platform
use_database = f"SELECT show_id FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%';"
cursor.execute(use_database)
record = cursor.fetchall()
print(record)
