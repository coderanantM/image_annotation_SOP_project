from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AnnotatedImage

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AnnotatedImage
        fields = ['title', 'original_image']