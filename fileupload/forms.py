from django import forms
from .models import FILE

class FileUploadForm(forms.Form):
    file=forms.FileField(label='upload your form')