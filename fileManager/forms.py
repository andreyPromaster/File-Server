from django import forms

from fileManager.models import UserContainer


class UploadFileForm(forms.ModelForm):
    file = forms.FileField(label="Upload file")
    email = forms.EmailField(required=False, label="Email", max_length=100)

    class Meta:
        model = UserContainer
        fields = ('email',)