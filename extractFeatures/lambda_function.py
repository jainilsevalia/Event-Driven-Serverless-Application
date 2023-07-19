import boto3
import nltk
import json
import os
import string
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# NLTK (Natural Language Toolkit) is a Python library used for natural language processing tasks, 
# offering tools and algorithms to work with human language data, including 
# tokenization, part-of-speech tagging, named entity recognition, and more.
nltk.data.path.append("./nltk_data")

# Created an instance of s3.
s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get the file details from uploded files on s3 bucket.
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    # Extract the file number from the file name 
    file_number = file_name.split('.')[0]

    # Read file content using get_s3_file_content mentioned function.
    file_content = get_s3_file_content(bucket_name, file_name)
    
    # Extract named entities from the file content using Natural Language Toolkit(nltk)
    named_entities = extract_named_entities(file_content)
    
    # Create the JSON array of named entities with frequencies which is output of eextract_named_entities function
    named_entities_json = create_named_entities_json(named_entities, file_name)
    
    # Save the JSON array as a file in the new bucket with updated name.
    save_named_entities_file(named_entities_json, file_number)

    return {
        'statusCode': 200,
        'body': 'Named entities extracted and saved successfully'
    }

def get_s3_file_content(bucket_name, file_name):
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response['Body'].read().decode('utf-8')
    return file_content


# Natural Language Toolkit (nltk) library in this code to extract named entities 
# from text by tokenizing and performing named entity recognition with 
# ne_chunk function, resulting in a JSON array with their frequencies.
def extract_named_entities(text):

    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Tag the tokens with their part-of-speech
    tagged_tokens = pos_tag(tokens)
    
    # Use ne_chunk to identify named entities
    named_entities = []

    # Reference : https://www.nltk.org/ 
    for chunk in ne_chunk(tagged_tokens):
        if isinstance(chunk, Tree):
            entity_name = ' '.join([token[0] for token in chunk])
            named_entities.append(entity_name)
    
    return named_entities

def create_named_entities_json(named_entities,file_name):
    named_entities_freq = {}

    for named_entity in named_entities:
        if named_entity not in named_entities_freq:
            named_entities_freq[named_entity] = 1
        else:
            named_entities_freq[named_entity] += 1
    
    file_name_with_ne = os.path.splitext(file_name)[0] + "ne" + os.path.splitext(file_name)[1]
    json_data = {file_name_with_ne: named_entities_freq}
    json_string = json.dumps(json_data)

    return json_string

def save_named_entities_file(named_entities_json, file_number):
    bucket_name = 'tags-b00925445' 
    file_name = f'{file_number}ne.txt'
    file_content = str(named_entities_json)
    
    # Upload the file to the new bucket
    s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
