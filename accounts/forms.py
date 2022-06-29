from django import forms
from .models import Profile


class UploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
