import uuid

from django.shortcuts import render
from FileServer import settings
from django.http import HttpResponseRedirect, HttpResponse

from .azure_storage_services import AzureStorageManager
from .forms import UploadFileForm
from .models import UserContainer, Content


def index(request):
    print(settings.CONNECTION_STRING_TO_AZURE_STORAGE)
    return render(request, "fileManager/index.html")


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
            container.email = form.cleaned_data["email"]  #?
            container.container = manager.container_name
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