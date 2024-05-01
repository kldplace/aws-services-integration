import os
import json
import boto3
import mysql.connector

def lambda_handler(event, context):
    # --- DATABASE CREDENTIALS ---
    host= os.environ['DB_HOST']
    database= os.environ['DB_DATABASE']
    user= os.environ['DB_USER']
    password= os.environ['DB_PASSWORD']

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
    # The [title withen director and release_year] SQL query of Saudi arabia movies in Netflix platform
    info_of_suadi_movies = f"SELECT title, director, release_year FROM {database}.shows WHERE type='Movie' AND country LIKE '%Saudi Arabia%' ORDER BY release_year;"
    cursor.execute(info_of_suadi_movies)
    records = cursor.fetchall()
    
    '''
    the reason of why i'm dealing with s3 Bucket here is becouse i want to read a data i stored on it,
    which is a json file inside a folder (json/saudi_movies_id_in_netflix.json), to get (show_id) of all
    movies from it, to combine it with the new information that i want it from previous query from RDS.
    +--------------------------------------------------------------------------------------------------------------+
    So the json file structure of the [show_id of saudi movies in netflix] it looks like:
    {
    "show_id": [
            {
            "1": "id_value"
            },
            {
            "2": "id_value"
            }
        ]
    }
    and the json file structure of the [info of saudi movies in netflix] it may looks like:
        {
    "saudi movies info": [
            {
            "1": [
                "title": "title_value", 
                "director": "director_value",
                "release_year": "release_year_value"
            ]
            },
            {
            "2": [
                "title": "title_value", 
                "director": "director_value",
                "release_year": "release_year_value"
            ]
            }
        ]
    }
    Now i want to combine that structure to looks like this:
            {
    "saudi movies info": [
            {
            "1": [
                "show_id": "id_value",
                "title": "title_value", 
                "director": "director_value",
                "release_year": "release_year_value"
            ]
            },
            {
            "2": [
                "show_id": "id_value",
                "title": "title_value", 
                "director": "director_value",
                "release_year": "release_year_value"
            ]
            }
        ]
    }
    +--------------------------------------------------------------------------------------------------------------+
    '''
    # --- S3 BUCKET ---
    # --- JSON FILE VARIABLES
    # [file_name_of_shows_info] it is the json file i want at the end to send it to s3 Bucket
    file_name_of_shows_info = 'saudi_movies_info_in_netflix.json'
    lambda_tmp_folder = "/tmp/"
    # --- BUCKET VARIABLES
    bucket_name = os.environ['S3_BUCKET']
    # [s3_folder] the folder i created in s3 Bucket
    s3_folder = 'json'
    key = f'{s3_folder}/{file_name_of_shows_info}'
    
    # --- READ AND GET DATA FROM S3 BUCKET ---
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    # to see the data that stored in [json/saudi_movies_id_in_netflix.json] in s3 Bucket
    for obj in bucket.objects.all():
        body = obj.get()['Body'].read().decode()
    '''
    to convert the [body] which is a (str) datatype to (dict) datatpe i used eval() function, to deal with it
    perfectly when i combine it with the result that coming from [info_of_suadi_movies] SQL 
    result from RDS.
    '''
    data = eval(body)
    '''
    set [length_of_list] variable to specify how many rows in this json file
    to use it in the nested loop, the number here is the same as the number of
    rows in the dataset in RDS from query result.
    
    i need this number to extract the (show_id) values from the dictionary,
    because the output of the [data] variable id dict([id_value]), and it store
    the data in nested list.
    
    i set the [show_id_list] variable to go through the values in nested loop
    and append it to [show_id_list].
    -- ** --
    i create [show_id_list] to handle [dict_values('show_id')] format using
    nested list comperhension to append a proprate values to [show_id_list].
    '''
    length_of_list = len(data["show_id"])
    show_id_list = []
    [[show_id_list.append(nested_val) for nested_val in list(data['show_id'][index].values())] for index in range(length_of_list)]

    '''
    [dict_info_of_suadi_movies] this dictionary it's the final result, it contains all
    info of saudi movies in netflix platform, i use [records] which is have my query result
    from RDS, and [show_id_list] which is have (show_id) values.
    so here i will combine the result from json file in s3 Bucket, and the result from RDS to make
    them in new json file that contain clear information about saudi movies in netflix platform,
    and send this new json file in s3 Bucket from lambda, as the structrue in README.md in this repo.
    '''
    dict_info_of_suadi_movies = {'suadi_movies_in_netflix': [] }
    num = 0
    index = -1 # to go through all the values in the [show_id_list]
    for r in records:
        num = num + 1
        index = index + 1
        query_values = str(r)[1:-1]
        query_values = query_values.split(',')
        dict_info_of_suadi_movies['suadi_movies_in_netflix'].append({num: {'show_id': show_id_list[index]  ,'movie': query_values[0][1:-1], 'director': query_values[1][2:-1], 'release_year': query_values[2][1:]}})
    # --- CREATE JSON FILE ---
    '''
    convert dictionary result that combine between data that comes from s3 Bucket
    and data comes from RDS to json format.
    '''
    info_as_json = json.dumps(dict_info_of_suadi_movies, indent=2)
    '''
    create a json file that store in 'tmp' folder, which is a temporary storage location provided by AWS Lambda. 
    It's where store temporary files during the execution of lambda function. 
    '''
    def create_json_file(file_name_of_shows_info, mode):
        with open(file_name_of_shows_info, mode) as jsonFile:
            jsonFile.write(info_as_json)
    create_json_file(f'{lambda_tmp_folder}saudi_movies_info_in_netflix.json', 'w') 
    # UPLOAD BUCKET
    # upload the json file i just created in the 'tmp' folder to the final destination, my s3 Bucket.
    def upload_to_s3_bucket(jsonFile, bucket_name, key):
        try:
            # key here is an organized way to put my (json file) inside a folder 
            s3.meta.client.upload_file(jsonFile, bucket_name, key)
            print("File Uploaded Succussfully")
        except Exception as error:
            print(error)
    upload_to_s3_bucket(f'{lambda_tmp_folder}{file_name_of_shows_info}', bucket_name, key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }