from django import forms
from .models import AppUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class ChangeUserForm(forms.ModelForm):

    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:

        model = AppUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')


class RegUserForm(forms.ModelForm):

    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, help_text='Повторите пожалуйства введёный ранее пароль')


    def clean_pass(self):
        
        password1 = self.cleaned_data['password1']

        if password1:

            password_validation.validate_password(password1)


    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
            'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = False
        if commit:
            user.save()
        #user_registered.send(RegisterUserForm, instance=user)
        return user


    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2',
        'first_name', 'last_name', 'send_message')


class search_form(forms.Form):
    
    query = forms.CharField()