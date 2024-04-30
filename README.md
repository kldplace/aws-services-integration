## AWS Services Integration
### Overview:
#### in this project i used a various AWS services, i used s3 Bucket, EC2, RDS, and lambda function, in this project i used a <a href="https://www.kaggle.com/datasets/shivamb/netflix-shows">Netflix Movies and TV Shows dataset </a>from kaggle to practice on these main services in AWS.

### Walking Through the Project:
<img src="./img/project_structure.png">

##### In this project i create:

* RDS (mysql server)
* S3 Bucket
* EC2 Instance
* Lambda Function

<hr>
<p> The structue of this project start from the <a href="https://www.kaggle.com/datasets/shivamb/netflix-shows"> dataset </a>i used from kaggle, I upload it to (mysql server) which i connected to AWS RDS service.</p>

<p>In EC2, I created a Python script to generate a JSON file and then placed it into an S3 Bucket.</p>

#### Packages used in the Python script:
| Package | Usage | Installation Command |
| --------| ------| ---------------------|
| mysql.connector | Connecting to MySQL databases | `pip install mysql-connector-python`|
| boto3 | Interacting with AWS services	 | `pip install boto3`|

In this script, I utilize the `sql.connector` package to execute a query aimed at retrieving the `show_id` of Saudi movies available on the Netflix platform. The result of this query is then formatted into a JSON file, which is uploaded to an S3 Bucket by utilize `boto3` package, specifically within the `json/` folder.

Finally, in the lambda function


