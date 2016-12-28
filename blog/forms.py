from django import forms

class UserInfo(forms.Form):
    username = forms.CharField(label= 'Username', max_length=100)
    # pay some attention about how to set password
    password = forms.CharField(label= 'Password', widget=forms.PasswordInput)
