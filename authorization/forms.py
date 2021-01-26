from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Никнейм')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Никнейм')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email_newsletters = forms.BooleanField(label='Почтовая рассылка', required=False, widget=forms.CheckboxInput(attrs={'checked': 'checked', 'id': 'email_newsletter'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts = {
            'username': ''
        }
        fields = ('username', 'email')


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        labels = {
            'picture': 'Изменить фото'
        }
        fields = ('picture',)


class NewslettersForm(forms.ModelForm):
    class Meta:
        model = Profile
        labels = {
            'email_newsletters': 'Email-рассылка'
        }
        fields = ('email_newsletters',)
