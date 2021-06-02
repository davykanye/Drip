from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, TextInput, EmailInput


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

        widgets = {
            'username': TextInput(attrs={
                'class': "t",
                'style': 'padding-left: 15px;background-color: rgba(234,234,235,0);',
                }),

            'email': EmailInput(attrs={
                'class': "t",
                'style': 'padding-left: 15px;background-color: rgba(234,234,235,0);',
                }),

            'first_name': TextInput(attrs={
                'class': "t",
                'style': 'padding-left: 15px;background-color: rgba(234,234,235,0);',
                }),

            'last_name': TextInput(attrs={
                'class': "t",
                'style': 'padding-left: 15px;background-color: rgba(234,234,235,0);',
                }),

        }
