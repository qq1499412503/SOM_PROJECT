from django import forms
from .models import dataframe


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = dataframe
        fields = ['data']

