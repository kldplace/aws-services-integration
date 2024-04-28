import os
from dotenv import load_dotenv
import json
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
id_of_suadi_movies = f"SELECT show_id FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"

cursor.execute(id_of_suadi_movies)
record = cursor.fetchall()

# DICTIONARY FRO QUIERY RESULT
dict_id_of_suadi_movies = {'show_id': []}
num = 0
for r in record:
    num = num + 1
    dict_id_of_suadi_movies['show_id'].append({num: str(r)[1:-2]})

# CONVERT QUEIRY RESULT TO JSON FORMAT
show_id_as_json = json.dumps(dict_id_of_suadi_movies, indent=2)
# CREATE JSON FILE
jsonFolder = "jsonFiles/"
with open(f'{jsonFolder}saudi_movies_id_in_netflix.json', 'w') as jsonFile:
    jsonFile.write(show_id_as_json)