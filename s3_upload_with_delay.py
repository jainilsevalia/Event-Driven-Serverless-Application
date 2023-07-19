import os
import time
import boto3
from tqdm import tqdm
# Create an S3 client Instance for uploading txt files
s3 = boto3.client('s3')
# Source and destination path are set to for txt files
destination_bucket_name = 'sample-data-b00925445'
source_folder_path = './tech' 
# Creating s3 bucket for pushing all txt file to the cloud
s3.create_bucket(Bucket=destination_bucket_name)
# Fetching the list of files form the source folder.
files = os.listdir(source_folder_path)

# Uploading files to the S3 bucket with a delay of 100 milliseconds
#I used this package for the loading bar.
#reference https://github.com/tqdm/tqdm 
with tqdm(total=len(files), unit='file') as pbar:
    for file_from_folder in files:
        file_path = os.path.join(source_folder_path, file_from_folder)

        # Upload the file to the S3 bucket using initiated s3 instance.
        s3.upload_file(file_path, destination_bucket_name, file_from_folder)

        # Update the progress bar
        pbar.update(1)

        # adding dealy of 100 miliseconds.
        time.sleep(0.1)
