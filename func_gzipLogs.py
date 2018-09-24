import json
import boto3
import gzip
import shutil
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try: 
        s3_client.download_file(bucket, key, '/tmp/file.log')
        with open('/tmp/file.log', 'rb') as f_in:
            with gzip.open('/tmp/data.log.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        s3_client.upload_file('/tmp/data.log.gz', bucket, key + '.gz')
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
