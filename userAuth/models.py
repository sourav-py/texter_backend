from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Profile(models.Model):
    phone = PhoneNumberField(null=False,blank=False,unique=True)
    date_joined = models.DateTimeField(auto_now_add =True)
    bio = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class OTPObject(models.Model):
    otp = models.CharField(null=False,blank=False,max_length=10) 
    phone = PhoneNumberField(null=False,blank=False)
    validTill = models.DateTimeField(null=False)


