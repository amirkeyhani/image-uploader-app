from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Profile, Comment

from django.contrib.auth import get_user_model

# Create your forms here.


class UploaderForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        exclude = ['like', 'created_at']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=150)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'email', 'text']
