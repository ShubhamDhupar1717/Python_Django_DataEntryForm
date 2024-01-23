from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import MemberData, MemberFamilyData, MemberAddressData, MemberBusinessData, ProposedMemberData



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
        labels = {
            "Fullname": "Full Name",
            "Dob": "Date of Birth",
            "Resphone": "Registered Phone No.",
            "Altermobileno": "Alternate Phone No.",
            "Officeno": "Office No.",
            "Resaddress": "Registered Address",
            }


# - Update member datails

class UpdateMemberData(forms.ModelForm):

    class Meta:

        model = MemberData
        fields = ['Fullname', 'Email', 'Dob', 'Resphone', 'Altermobileno', 'Resaddress', 'Officeno', 'Country', 'Profilepic', 'Signature']
        labels = {
            "Fullname": "Full Name",
            "Dob": "Date of Birth",
            "Resphone": "Registered Phone No.",
            "Altermobileno": "Alternate Phone No.",
            "Officeno": "Office No.",
            "Resaddress": "Registered Address",
            }



# - Create a member family data

class CreateMemberFamilyData(forms.ModelForm):

    class Meta:

        model = MemberFamilyData
        fields = ['firstname', 'lastname', 'relation', 'contactno', 'homeaddress', 'Spousename', 'Spousedob', 'Childname']
        labels = {
            "Firstname": "First Name",
            "Lastname": "Last Name",
            "contactno": "Contact Number",
            "Spousename": "Spouse Name",
            "Spousedob": "Spouse D.O.B",
            "homeaddress": "Home Address",
            }


# - Update member family data

class UpdateMemberFamilyData(forms.ModelForm):

    class Meta:

        model = MemberFamilyData
        fields = ['firstname', 'lastname', 'relation', 'contactno', 'homeaddress', 'Spousename', 'Spousedob', 'Childname']
        labels = {
            "Firstname": "First Name",
            "Lastname": "Last Name",
            "contactno": "Contact Number",
            "Spousename": "Spouse Name",
            "Spousedob": "Spouse D.O.B",
            "homeaddress": "Home Address",
            }





# - Create a member address data

class CreateMemberAddressData(forms.ModelForm):

    class Meta:

        model = MemberAddressData
        fields = ['Address', 'Country', 'State', 'City', 'Postalcode', 'Addresstype', 'Additionalinfo']
        labels = {
            "Addresstype": "Address Type",
            "Additionalinfo": "Additional Information",
            }


# - Update member address data

class UpdateMemberAddressData(forms.ModelForm):

    class Meta:

        model = MemberAddressData
        fields = ['Address', 'Country', 'State', 'City', 'Postalcode', 'Addresstype', 'Additionalinfo']
        labels = {
            "Addresstype": "Address Type",
            "Additionalinfo": "Additional Information",
            }





# - Create a member business data

class CreateMemberBusinessData(forms.ModelForm):

    class Meta:

        model = MemberBusinessData
        fields = ['Businessname', 'Businessdetails', 'Businessaddress', 'Businesscity', 'Businessemail', 'Businesspostalcode']
        labels = {
            "Businessname": "Business Name",
            "Businessdetails": "Business Details",
            "Businessaddress": "Business Address",
            "Businesscity": "Business City",
            "Businessemail": "Business Email",
            "Businesspostalcode": "Business Postal Code",
            }


# - Update member business data

class UpdateMemberBusinessData(forms.ModelForm):

    class Meta:

        model = MemberBusinessData
        fields = ['Businessname', 'Businessdetails', 'Businessaddress', 'Businesscity', 'Businessemail', 'Businesspostalcode']
        labels = {
            "Businessname": "Business Name",
            "Businessdetails": "Business Details",
            "Businessaddress": "Business Address",
            "Businesscity": "Business City",
            "Businessemail": "Business Email",
            "Businesspostalcode": "Business Postal Code",
            }










class ProposedMemberDataForm(forms.ModelForm):
    class Meta:
        model = ProposedMemberData
        fields = ['Fullname', 'Email', 'Dob', 'Resphone', 'Altermobileno', 'Resaddress', 'Officeno', 'Country', 'Profilepic', 'Signature']
        labels = {
            "Fullname": "Full Name",
            "Dob": "Date of Birth",
            "Resphone": "Registered Phone No.",
            "Altermobileno": "Alternate Phone No.",
            "Officeno": "Office No.",
            "Resaddress": "Registered Address",
            }
        


class ProposedMemberFamilyDataForm(forms.ModelForm):
    class Meta:
        model = ProposedMemberData
        fields = ['firstname', 'lastname', 'relation', 'contactno', 'homeaddress', 'Spousename', 'Spousedob', 'Childname']
        labels = {
            "Firstname": "First Name",
            "Lastname": "Last Name",
            "contactno": "Contact Number",
            "Spousename": "Spouse Name",
            "Spousedob": "Spouse D.O.B",
            "homeaddress": "Home Address",
            }
                        


class ProposedMemberAddressDataForm(forms.ModelForm):
    class Meta:
        model = ProposedMemberData
        fields = ['Address', 'Country', 'State', 'City', 'Postalcode', 'Addresstype', 'Additionalinfo']
        labels = {
            "Addresstype": "Address Type",
            "Additionalinfo": "Additional Information",
            }
        


class ProposedMemberBusinessDataForm(forms.ModelForm):
    class Meta:
        model = ProposedMemberData
        fields = ['Businessname', 'Businessdetails', 'Businessaddress', 'Businesscity', 'Businessemail', 'Businesspostalcode']
        labels = {
            "Businessname": "Business Name",
            "Businessdetails": "Business Details",
            "Businessaddress": "Business Address",
            "Businesscity": "Business City",
            "Businessemail": "Business Email",
            "Businesspostalcode": "Business Postal Code",
            }

        

        