from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise forms.ValidationError('Incorrect username and/or password.')

        return self.cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=25, label='Username')
    email = forms.EmailField(max_length=30, label='Email',
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'at least 8 characters'}),
                               label='Password')
    password_confirmed = forms.CharField(widget=forms.PasswordInput,
                                         label='Confirm password')

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmed')

        if password and password != password_confirmation:
            raise forms.ValidationError("Passwords don't match.")

        return self.cleaned_data
