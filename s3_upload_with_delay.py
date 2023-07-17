import os
import time
import boto3
from tqdm import tqdm

# Create an S3 client
s3 = boto3.client('s3')

# Define the bucket name and folder path
bucket_name = 'sample-data-b00925445'
folder_path = './tech' 

# Create the S3 bucket
s3.create_bucket(Bucket=bucket_name)

# Get a list of files in the folder
files = os.listdir(folder_path)

# Upload files to the S3 bucket with a delay of 100 milliseconds
with tqdm(total=len(files), unit='file') as pbar:
    for file_from_folder in files:
        # Construct the file path
        file_path = os.path.join(folder_path, file_from_folder)

        # Upload the file to the S3 bucket
        s3.upload_file(file_path, bucket_name, file_from_folder)

        # Update the progress bar
        pbar.update(1)

        # Wait for 100 milliseconds before the next upload
        time.sleep(0.1)
