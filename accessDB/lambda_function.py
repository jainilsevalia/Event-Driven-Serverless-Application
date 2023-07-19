import boto3
import json

# Created an instance of DynamoDB.
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):

    # Get the bucket and file information from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    # Fetching the named entity JSON file content from S3
    file_content = get_s3_file_content(bucket_name, file_name)
    
    # Parse the JSON content
    named_entities = json.loads(file_content)
    
    # Update the DynamoDB table with the named entities
    update_dynamodb_table(named_entities)
    
    return {
        'statusCode': 200,
        'body': 'DynamoDB table updated successfully'
    }

def get_s3_file_content(bucket_name, file_name):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response['Body'].read().decode('utf-8')
    return file_content

def update_dynamodb_table(named_entities):
    for key, value in named_entities.items():
        for entity, frequency in value.items():
            item = {
                'Entity': {'S': entity},
                'Frequency': {'S': str(frequency)}
            }

            dynamodb.put_item(
                TableName='Named_Entities_Frequency',
                Item=item
            )

