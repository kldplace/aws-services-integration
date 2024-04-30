import os
from dotenv import load_dotenv
import json
import boto3

load_dotenv()

file_name = 'saudi_movies_id_in_netflix.json'
jsonFolder = "../jsonFiles/"
bucket_name = os.getenv('S3_BUCKET')
s3_folder = 'json'
# key = f'{s3_folder}/{file_name}'

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
for obj in bucket.objects.all():
    body = obj.get()['Body'].read().decode()

# with open(jsonFolder+file_name, "r") as jsonFile:
#     data = json.load(jsonFile)
data = eval(body)
print(data)
# length_of_list = len(data["show_id"])
# print(length_of_list)