import boto3
import json

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Get the bucket and file information from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    print("====================================================Bucket Name============================")
    print(bucket_name)

    file_name = event['Records'][0]['s3']['object']['key']
    print("===============================================File name============================")
    print(file_name)
    # Read the named entity JSON file content from S3
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

    print("================================================S3 _ file response=======================================")
    print(response)
    file_content = response['Body'].read().decode('utf-8')

    print("=============================================file content ==========================================")
    print(file_content)
    return file_content

def update_dynamodb_table(named_entities):
    print("=============================================== Outside for loop ================================")
    for key, value in named_entities.items():
        print("==========================inside for loop ==============================")
        for entity, frequency in value.items():
            item = {
                'Entity': {'S': entity},
                'Frequency': {'S': str(frequency)}
            }

            print("=========================================Item ================================")
            print(item)
        
            print("==================================uploading this item =======================")
            dynamodb.put_item(
                TableName='Named_Entities_Frequency',
                Item=item
            )

    print("=====================================================all data should be in DB ===========================")
