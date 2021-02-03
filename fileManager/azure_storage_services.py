import os
import uuid

from azure.storage.blob import BlobServiceClient, BlobClient
from FileServer import settings


class AzureStorageManager:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING_TO_AZURE_STORAGE)

    def create_container(self):
        self.container_name = self.__create_unique_string()
        self.blob_service_client.create_container(self.container_name)

    def __create_unique_string(self):
        return str(uuid.uuid4())

    def upload_file_to_container(self, file, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

        # Upload the created file
        for chunk in file.chunks():
            blob_client.upload_blob(chunk)


# # Download the blob to a local file
# # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
# download_file_path = os.path.join(local_path, str.replace(local_file_name, '.txt', 'DOWNLOAD.txt'))
# print("\nDownloading blob to \n\t" + download_file_path)
#
# with open(download_file_path, "wb") as download_file:
#     download_file.write(blob_client.download_blob().readall())
