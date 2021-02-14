import uuid

from django.shortcuts import get_object_or_404
from io import BytesIO
from fileManager.azure_storage_services import AzureStorageManager
from fileManager.models import Content, UserContainer


def get_data_from_azure_storage(unique_link_to_blob):
    """ Get data from created container via link """
    file_storage = get_object_or_404(Content, unique_link_to_blob=unique_link_to_blob)
    storage_manager = AzureStorageManager()
    data = BytesIO(storage_manager.download_file_from_storage(str(file_storage.container.name_container),
                                                              str(file_storage.name_of_blob)))
    data.name = str(file_storage.name_of_blob)
    return data


def get_azure_container_by_email(email):
    query = UserContainer.objects.filter(email=email)
    if query.exists():
        return query[0]


def get_azure_container_by_cookies(request):
    if request.COOKIES.get("container") is not None:
        query = UserContainer.objects.filter(name_container=request.COOKIES.get("container"))
        if query.exists():
            return query[0]


def create_container_in_db(email, current_container_name):
    """Save info about Azure container into db"""

    current_container = UserContainer()
    current_container.email = email
    current_container.name_container = current_container_name
    current_container.save()
    return current_container


def create_blob_into_container(container, file_name):
    """Save info about blob into db"""

    blob = Content()
    blob.container = container
    blob.name_of_blob = file_name
    blob.unique_link_to_blob = str(uuid.uuid4())
    blob.save()
    return blob

def create_related_container_to_azure_storage(email):
    """Create Azure container and links with record in db"""

    manager = AzureStorageManager()
    manager.create_container()
    return create_container_in_db(email, manager.get_current_container())


def create_file_name_for_uploaded_file(current_file_name):
    file_name = str(uuid.uuid4())
    return file_name + "." + current_file_name.split(".")[-1]


def upload_file_to_azure_container(container_name, file, file_name):
    manager = AzureStorageManager(container_name)
    manager.upload_file_to_container(file, file_name)


def find_container_or_create(request, email):
    """Find info about azure container in cookies or email and
    return container object """
    if email != "":
        current_container = get_azure_container_by_email(email)
    else:
        current_container = get_azure_container_by_cookies(request)

    if current_container is None:
        current_container = create_related_container_to_azure_storage(email=email)

    return current_container


