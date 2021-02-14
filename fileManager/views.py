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

from .services import get_data_from_azure_storage, get_azure_container_by_email, get_azure_container_by_cookies, \
    create_container_in_db, create_related_container_to_azure_storage, upload_file_to_azure_container, \
    create_file_name_for_uploaded_file, create_blob_into_container, find_container_or_create


def index(request):
    print(settings.CONNECTION_STRING_TO_AZURE_STORAGE)
    return render(request, "fileManager/index.html")


def download_file(request, unique_link_to_blob):
    return FileResponse(get_data_from_azure_storage(unique_link_to_blob),
                        as_attachment=True)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            current_email = form.cleaned_data["email"]

            current_container = find_container_or_create(request, current_email)

            file_name = create_file_name_for_uploaded_file(request.FILES['file'].name)
            upload_file_to_azure_container(str(current_container.name_container),
                                           request.FILES['file'],
                                           file_name)

            blob = create_blob_into_container(current_container, file_name)

            form = UploadFileForm()
            url = reverse("download_file", kwargs={"unique_link_to_blob": blob.unique_link_to_blob})
            response = render(request, 'fileManager/index.html', {'form': form, "uploaded_file_url": url})
            response.set_cookie(key='container', value=current_container.name_container, max_age=50000000)
            return response
    else:
        form = UploadFileForm()
    return render(request, 'fileManager/index.html', {'form': form})
