from django import forms

from fileManager.models import UserContainer


class UploadFileForm(forms.ModelForm):
    file = forms.FileField(label="Upload file")

    class Meta:
        model = UserContainer
        fields = ('email',)