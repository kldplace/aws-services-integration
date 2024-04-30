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

# --- S3 BUCKET ---
# --- JSON FILE VARIABLES
file_name = 'saudi_movies_id_in_netflix.json'
jsonFolder = "../jsonFiles/"
# --- BUCKET VARIABLES
bucket_name = os.getenv('S3_BUCKET')
s3_folder = 'json'
key = f'{s3_folder}/{file_name}'

# --- READ FROM S3 BUCKET ---
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

for obj in bucket.objects.all():
    body = obj.get()['Body'].read().decode()
    

# SET MySQL CURSOR
cursor = connection.cursor()

# --- MY QUERIES ---
# The [title withen director and release_year] of Saudi arabia movies in Netflix platform
info_of_suadi_movies = f"SELECT title, director, release_year FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"

cursor.execute(info_of_suadi_movies)
records = cursor.fetchall()

# DICTIONARY FRO QUIERY RESULT
# to read from json file
with open(jsonFolder+file_name, "r") as jsonFile:
    data = json.load(jsonFile)
'''
length of list to specify how many rows do we have in this json file
as we shown when we querying the saudi [show_id] in netflix platform.
-- ** --
i create [show_id_list] to handle [dict_values('show_id')] format using
nested list comperhension to append a proprate values to [show_id_list].
'''
length_of_list = len(data["show_id"])
show_id_list = []
saudi_show_id = [[show_id_list.append(nested_val) for nested_val in list(data['show_id'][index].values())] for index in range(length_of_list)]


dict_info_of_suadi_movies = {'suadi_movies_in_netflix': [] }
num = 0
index = -1
for r in records:
    num = num + 1
    index = index + 1
    query_values = str(r)[1:-1]
    query_values = query_values.split(',')
    dict_info_of_suadi_movies['suadi_movies_in_netflix'].append({num: {'show_id': show_id_list[index]  ,'movie': query_values[0][1:-1], 'director': query_values[1][2:-1], 'release_year': query_values[2][1:]}})

# --- CREATE JSON FILE ---
# CONVERT QUEIRY RESULT TO JSON FORMAT
show_info_as_json = json.dumps(dict_info_of_suadi_movies, indent=2)
'''
after merging the [show_id] from json file with the new query that 
showing [title, director, and release_year] i created function here to 
create a json file for saudi movies in netflix platform that showing:
show_id, title, director and release_year
'''
def create_json_file(file_name, mode):
    with open(file_name, mode) as jsonFile:
        jsonFile.write(show_info_as_json)
create_json_file(f'{jsonFolder}saudi_movies_info_in_netflix.json', 'w')    
        