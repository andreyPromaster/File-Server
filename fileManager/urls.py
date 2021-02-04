from django.urls import path

from .views import upload_file, download_file

urlpatterns = [
    path("", upload_file),
    path('files/<uuid:unique_link_to_blob>', download_file, name="download file"),

]
