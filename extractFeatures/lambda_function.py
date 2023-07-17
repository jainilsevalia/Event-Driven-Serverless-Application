import boto3
import nltk
import json
import os

# nltk.download('punkt')
nltk.data.path.append("./nltk_data")
import string
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

# Create an S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print("================================EVENT=============================")
    print(event)
    # Get the uploaded file details from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    print("==========================Bucket_name=========================")
    print(bucket_name)
    file_name = event['Records'][0]['s3']['object']['key']
    print("====================================file_name=====================")
    print(file_name)
    
    # Extract the file number from the file name (e.g., "001.txt" -> "001")
    file_number = file_name.split('.')[0]
    print("============================File_Number")
    print(file_number)

    # Read the file content from S3
    file_content = get_s3_file_content(bucket_name, file_name)
    print("====================================COntent========================")
    print(file_content)
    
    # Extract named entities from the file content
    named_entities = extract_named_entities(file_content)
    print("===============================Named Entities===========================")
    print(named_entities)
    
    # Create the JSON array of named entities with frequencies
    named_entities_json = create_named_entities_json(named_entities, file_name)
    print("===============================Json_array=========================")
    print(named_entities_json)
    
    print("==================Saving Entities ===================")
    # Save the JSON array as a file in the new bucket
    save_named_entities_file(named_entities_json, file_number)

    return {
        'statusCode': 200,
        'body': 'Named entities extracted and saved successfully'
    }

def get_s3_file_content(bucket_name, file_name):
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    print("=========================response of s3====================")
    print(response)

    file_content = response['Body'].read().decode('utf-8')
    print("===========================Readind file content================")
    print(file_content)
    return file_content

def extract_named_entities(text):

    print("===================Started Tokenizing words=====================")
    # Tokenize the text
    tokens = word_tokenize(text)
    print("=============================Tokens========================")
    print(tokens)
    
    print("============================Taging tokens=================")
    # Tag the tokens with their part-of-speech
    tagged_tokens = pos_tag(tokens)
    print("=================================Taged Tokens =======================")
    print(tagged_tokens)
    
    print("===============================Outside For loop =====================")
    # Use ne_chunk to identify named entities
    named_entities = []
    for chunk in ne_chunk(tagged_tokens):
        print("===================================Inside for loop ==============================")
        if isinstance(chunk, Tree):
            print("=======================================Inside if loop ======================")
            entity_name = ' '.join([token[0] for token in chunk])
            print("============================entity _name ===============================")
            print(entity_name)
            named_entities.append(entity_name)
    
    print("=============================Printing all entities ================================")
    print(named_entities)
    return named_entities

def create_named_entities_json(named_entities,file_name):
    named_entities_freq = {}
    print("===================outside for loop ==================")
    for named_entity in named_entities:
        print("=====================inside for loop =====================")
        if named_entity not in named_entities_freq:
            print("============================inside if loop ==================")
            named_entities_freq[named_entity] = 1
        else:
            print("================================ Inside else loop =====================")
            named_entities_freq[named_entity] += 1
    
    file_name_with_ne = os.path.splitext(file_name)[0] + "ne" + os.path.splitext(file_name)[1]

    json_data = {file_name_with_ne: named_entities_freq}
    json_string = json.dumps(json_data)

    print("====================================json_string ============================")
    print(json_string)
    return json_string

def save_named_entities_file(named_entities_json, file_number):
    bucket_name = 'tags-b00925445'  # Replace with the new bucket name
    file_name = f'{file_number}ne.txt'
    print("===============================re-tagging file name =========================")
    print(file_name)
    file_content = str(named_entities_json)
    
    print("======================uploading file=========================")
    # Upload the file to the new bucket
    s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
