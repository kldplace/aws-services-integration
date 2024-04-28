import os
from dotenv import load_dotenv
import json
import boto3
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
# The [title withen director and release_year] of Saudi arabia movies in Netflix platform
info_of_suadi_movies = f"SELECT title, director, release_year FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"

cursor.execute(info_of_suadi_movies)
record = cursor.fetchall()

# --- S3 BUCKET ---
file_name = 'saudi_movies_id_in_netflix.json'
bucket_name = os.getenv('S3_BUCKET')
s3_folder = 'input'
key = f'{s3_folder}/{file_name}'

# --- READ FROM S3 BUCKET ---
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(bucket_name)

# for obj in bucket.objects.all():
#     body = obj.get()['Body'].read().decode()
#     print(body)