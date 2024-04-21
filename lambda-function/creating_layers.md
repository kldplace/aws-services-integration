## Steps of creating a lambda layers:
- First create this series of directories.<br>
`mkdir -p python/lib/python3.9/site-packages`

- Create a `requirements.txt` file.

- Write the packages you need for your lambda to `requirements.txt`file, in my case i need to:<br>
`boto3==1.34.46
mysql.connector==2.2.9`

- Install the packages you just write it in the last step into the series of directories we created in the first step by this command:<br>
`pip install -r requirements.txt -t python/lib/python3.9/site-packages`

- Zip the packages that you are install with this command:<br>
`zip -r <packages_name>.zip python`

- Publish the layer in AWS lambda function. <br>
`aws lambda publish-layer-version \
    --layer-name <my_layer_name> \
    --compatible-runtimes python3.9 \
    --zip-file fileb://<packages_name>.zip`