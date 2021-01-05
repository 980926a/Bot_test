import os
import uuid
import re
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime

# import pandas as pd


connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

print(connect_str)

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Instantiate a ContainerClient
container_client = blob_service_client.get_container_client("smartwatchdata")

blobs_filename_list = container_client.list_blobs()

# print(blobs_filename_list)
now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')
# print(now)          # 2018-07-28 12:11:32.669083


# print(nowDate)      # 2018-07-28.


new_blob = list()
post_num = 0

while True:

    for blob_filename in blobs_filename_list:
        if re.match(nowDate, blob_filename.name):
            new_blob.append(blob_filename.name)

    # print(new_blob)

    if(post_num != len(new_blob)):

        late_num = int(len(new_blob))

        for i in range(post_num,late_num):
            print("Update File : " + new_blob[i])

        post_num = len(new_blob)


    time.sleep(100)


