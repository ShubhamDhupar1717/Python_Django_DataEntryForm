from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import MemberData



# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']



# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a member

class CreateMemberData(forms.ModelForm):

    class Meta:

        model = MemberData
        fields = ['Fullname', 'Email', 'Dob', 'Resphone', 'Altermobileno', 'Resaddress', 'Officeno', 'Country', 'Profilepic', 'Signature']


# - Update member datails

class UpdateMemberData(forms.ModelForm):

    class Meta:

        model = MemberData
        fields = ['Fullname', 'Email', 'Dob', 'Resphone', 'Altermobileno', 'Resaddress', 'Officeno', 'Country', 'Profilepic', 'Signature']


