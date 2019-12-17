from django import forms

class UploadFileForm(forms.Form):
    linux_file = forms.FileField(label='Upload file')
