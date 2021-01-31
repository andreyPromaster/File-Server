from django.shortcuts import render


# Create your views here.
from FileServer import settings


def index(request):
    print(settings.CONNECTION_STRING_TO_AZURE_STORAGE)
    return render(request, "fileManager/index.html")
