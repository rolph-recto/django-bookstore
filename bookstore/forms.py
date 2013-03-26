#bookstore/forms.py
#Rolph Recto

from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def clean(self):
        """authenticate the user info"""
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            #check if user is active
            if not user.is_active:
                raise forms.ValidationError('This account is disabled.')
        else:
            raise forms.ValidationError('Invalid user information.')

        return cleaned_data

