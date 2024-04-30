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
# The [show_id] SQL query of Saudi arabia movies in Netflix platform
id_of_suadi_movies = f"SELECT show_id FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"
cursor.execute(id_of_suadi_movies)
records = cursor.fetchall()

# DICTIONARY FRO QUIERY RESULT
'''
here i create a dictionay to store the (show_id) that come from last query
wihich is (records) variable.
'''
dict_id_of_suadi_movies = {'show_id': []}
num = 0
for r in records:
    num = num + 1
    dict_id_of_suadi_movies['show_id'].append({num: str(r)[2:-3] }) # (str(r)[2:-3]) this syntax to clean the result that come from (records)

# --- CREATE JSON FILE ---
# CONVERT DICT RESULT TO JSON FORMAT
show_id_as_json = json.dumps(dict_id_of_suadi_movies, indent=2)
# CREATE JSON FILE
json_files_folder = "jsonFiles/"
with open(f'{json_files_folder}saudi_movies_id_in_netflix.json', 'w') as jsonFile:
    jsonFile.write(show_id_as_json)
    
# --- CREATE AND UPLOAD TO AWS S3 BUCKET ---
s3 = boto3.resource('s3')
# --- BUCKET VARIABLES
file_name = 'saudi_movies_id_in_netflix.json'
bucket_name = os.getenv('S3_BUCKET')
LocationConstraint = os.getenv('REGION')
s3_folder = 'json'
key = f'{s3_folder}/{file_name}'

# CREATE BUCKET FUNCTION
def create_s3_bucket(bucket_name, region):
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region,
            })
        print('s3 Bucket created successfully')
    except Exception as error:
        print(error)
# UPLOAD BUCKET FUNCTION
def upload_to_s3_bucket(jsonFile, bucket_name, key):
    try:
        # key here is an organized way to put my (json file) inside a folder 
        s3.meta.client.upload_file(jsonFile, bucket_name, key)
        print("File Uploaded Succussfully")
    except Exception as error:
        print(error)
        
create_s3_bucket(bucket_name,LocationConstraint)
upload_to_s3_bucket(json_files_folder + file_name, bucket_name, key)
