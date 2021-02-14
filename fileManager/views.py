from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from FileServer import settings
from .forms import UploadFileForm
from .services import get_data_from_azure_storage, upload_file_to_azure_container, \
    create_file_name_for_uploaded_file, create_blob_into_container, find_or_create_container


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
            current_container = find_or_create_container(request, current_email)

            file_name = create_file_name_for_uploaded_file(request.FILES['file'].name)
            upload_file_to_azure_container(str(current_container.name_container),
                                           request.FILES['file'],
                                           file_name)

            blob = create_blob_into_container(current_container, file_name)
            url = reverse("download_file", kwargs={"unique_link_to_blob": blob.unique_link_to_blob})
            if current_email != "":
                send_mail('Ссылка на Ваш файл', request.build_absolute_uri(url),
                          settings.EMAIL_HOST_USER, [current_email])

            response = render(request, 'fileManager/index.html',
                              {'form': UploadFileForm(), "uploaded_file_url": url})
            
            response.set_cookie(key='container', value=current_container.name_container,
                                max_age=50000000)
            return response
    else:
        form = UploadFileForm()
    return render(request, 'fileManager/index.html', {'form': form})
