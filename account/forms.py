from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=12,
        help_text='Required. 12 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Re-enter Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 12:
            raise forms.ValidationError('Username must be 12 characters or fewer.')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
