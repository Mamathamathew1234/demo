from django import forms
from .models import *

# Create your formss here.

class UserProfileForm(forms.Form):
    Name =forms.CharField()
    User_Name = forms.CharField()
    User_Email = forms.EmailField()
    UserPhone = forms.IntegerField()
    Password = forms.CharField()
    u_address = forms.CharField()
    u_district = forms.CharField()
    u_city = forms.CharField()
    u_pincode = forms.IntegerField()

class DelboyProfileForm(forms.Form):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=50)
    phone = models.IntegerField()
    photo= models.FileField()
    license = models.FileField()
    biodata = models.FileField()
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=10)
