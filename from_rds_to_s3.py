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
# The [show_id] of Saudi arabia movies in Netflix platform
id_of_suadi_movies = f"SELECT show_id FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"

cursor.execute(id_of_suadi_movies)
record = cursor.fetchall()

# DICTIONARY FRO QUIERY RESULT
dict_id_of_suadi_movies = {'show_id': []}
num = 0
for r in record:
    num = num + 1
    dict_id_of_suadi_movies['show_id'].append({num: str(r)[2:-3]})

# --- CREATE JSON FILE ---
# CONVERT QUEIRY RESULT TO JSON FORMAT
show_id_as_json = json.dumps(dict_id_of_suadi_movies, indent=2)

# CREATE JSON FILE
jsonFolder = "jsonFiles/"
with open(f'{jsonFolder}saudi_movies_id_in_netflix.json', 'w') as jsonFile:
    jsonFile.write(show_id_as_json)
    
# --- CREATE AND UPLOAD TO AWS S3 BUCKET ---
s3 = boto3.resource('s3')
# --- BUCKET VARIABLES
file_name = 'saudi_movies_id_in_netflix.json'
bucket_name = os.getenv('S3_BUCKET')
LocationConstraint = os.getenv('REGION')
s3_folder = 'input'
key = f'{s3_folder}/{file_name}'

# CREATE BUCKET
def create_s3_bucket(bucket_name, region):
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region,
            })
        print('s3 Bucket created successfully')
    except Exception as error:
        print(error)
# create_s3_bucket(bucket_name,LocationConstraint)

# UPLOAD BUCKET
def upload_to_s3_bucket(jsonFile, bucket_name, key):
    try:
        # key here is an organized way to put my (json file) inside a folder 
        s3.meta.client.upload_file(jsonFile, bucket_name, key)
        print("File Uploaded Succussfully")
    except Exception as error:
        print(error)
upload_to_s3_bucket(jsonFolder + file_name, bucket_name, key)
