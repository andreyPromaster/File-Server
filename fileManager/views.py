import os
import tempfile
import uuid
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    file_storage = get_object_or_404(Content, unique_link_to_blob=unique_link_to_blob)
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
            current_container = ""
            current_email = form.cleaned_data["email"]

            if current_email != "":
                query = UserContainer.objects.filter(email=current_email)
                if query.exists():
                    current_container = query[0]
            else:
                if request.COOKIES.get("container") is not None:
                    query = UserContainer.objects.filter(name_container=request.COOKIES.get("container"))
                    if query.exists():
                        current_container = query[0]

            if current_container == "":
                manager = AzureStorageManager()
                manager.create_container()
                current_container = UserContainer()
                current_container.email = current_email
                current_container.name_container = manager.get_current_container()
                current_container.save()
            else:
                manager = AzureStorageManager(str(current_container.name_container))

            file_name = str(uuid.uuid4())
            file = request.FILES['file']
            file_name = file_name + "." + file.name.split(".")[-1]
            manager.upload_file_to_container(file, file_name)

            blob = Content()
            blob.container = current_container
            blob.name_of_blob = file_name
            blob.unique_link_to_blob = str(uuid.uuid4())
            blob.save()

            form = UploadFileForm()
            url = reverse("download_file", kwargs={"unique_link_to_blob": blob.unique_link_to_blob})
            response = render(request, 'fileManager/index.html', {'form': form, "uploaded_file_url": url})
            response.set_cookie(key='container', value=manager.get_current_container(), max_age=50000000)
            return response
    else:
        form = UploadFileForm()
    return render(request, 'fileManager/index.html', {'form': form})
