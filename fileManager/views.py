import os
import tempfile
import uuid
from io import BytesIO

from django.shortcuts import render


from FileServer import settings
from django.http import HttpResponseRedirect, HttpResponse, FileResponse

from .azure_storage_services import AzureStorageManager
from .forms import UploadFileForm
from .models import UserContainer, Content
from django.db.models import signals
from django.dispatch import receiver

def index(request):
    print(settings.CONNECTION_STRING_TO_AZURE_STORAGE)
    return render(request, "fileManager/index.html")


def download_file(request, unique_link_to_blob):
    file_storage = Content.objects.get(unique_link_to_blob=unique_link_to_blob)
    storage_manager = AzureStorageManager()

    data = storage_manager.download_file_from_storage(str(file_storage.container.name_container),
                                                      str(file_storage.name_of_blob))

    return FileResponse(BytesIO(data),
                        as_attachment=True,
                        filename=str(file_storage.name_of_blob))


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            manager = AzureStorageManager()
            manager.create_container()
            file_name = str(uuid.uuid4())
            file = request.FILES['file']
            file_name = file_name + "." + file.name.split(".")[-1]
            manager.upload_file_to_container(file, file_name)

            container = UserContainer()
            container.email = form.cleaned_data["email"]  # ?
            container.name_container = manager.get_current_container()
            container.save()

            blob = Content()
            blob.container = container
            blob.name_of_blob = file_name
            blob.unique_link_to_blob = str(uuid.uuid4())
            blob.save()

            return HttpResponse('<p>ok</p>')
    else:
        form = UploadFileForm()
    return render(request, 'fileManager/index.html', {'form': form})
