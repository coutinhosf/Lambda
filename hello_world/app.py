import io
import urllib.parse
import boto3
import json
import pandas as pd

def lambda_handler(event, context):

    try:
        # print('Loading function')
        HOST = "http://host.docker.internal"
        # Get the service resource
        # To production it's not necessary inform the "endpoint_url" and "region_name"
        s3 = boto3.client("s3", endpoint_url=HOST + ":4566", region_name="us-east-1")

        # print("Received event: " + json.dumps(event, indent=2))
        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read()
        data = io.BytesIO(data)
        deb = {
            "request_id": response['ResponseMetadata']['RequestId'],
            "key": key,
            "bucket": bucket,
            "message": "aws lambda with localstack...",
            "dadosExcel": data
        }
    except Exception as e:
        print(e)
        raise e

    print("Final Output: {}".format(json.dumps(deb)))
    return json.dumps(deb)
