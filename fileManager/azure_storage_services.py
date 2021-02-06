import os
import uuid

from azure.storage.blob import BlobServiceClient
import tempfile
from FileServer import settings


class AzureStorageManager:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING_TO_AZURE_STORAGE)

    def create_container(self):
        self.container_name = self.__create_unique_string()
        self.blob_service_client.create_container(self.container_name)

    def __create_unique_string(self):
        return str(uuid.uuid4())

    def get_current_container(self):
        return self.container_name

    def upload_file_to_container(self, file, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

        # Upload the created file
        for chunk in file.chunks():
            blob_client.upload_blob(chunk)

    def download_file_from_storage(self, container, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=container, blob=file_name)
        data = blob_client.download_blob().readall()
        return data


