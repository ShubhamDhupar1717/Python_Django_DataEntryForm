from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberData(models.Model):

    Fullname = models.CharField(max_length=100)

    Email = models.CharField(max_length=250)

    Dob = models.DateTimeField()

    Resphone = models.CharField(max_length=20)

    Altermobileno = models.CharField(max_length=20)

    Resaddress = models.CharField(max_length=300)

    Officeno = models.CharField(max_length=255)

    Country = models.CharField(max_length=125)

    Profilepic = models.ImageField(upload_to='pics')

    Signature = models.ImageField(upload_to='pics')
    
    Creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Fullname
    


class MemberFamilyData(models.Model):

    firstname = models.CharField(max_length=100)

    lastname = models.CharField(max_length=100)

    relation = models.CharField(max_length=100)

    contactno = models.CharField(max_length=20)

    homeaddress = models.CharField(max_length=300)

    Spousename = models.CharField(max_length=200)

    Spousedob = models.DateTimeField()

    Childname = models.CharField(max_length=100)
    
    member = models.ForeignKey(MemberData, on_delete=models.CASCADE)





class MemberAddressData(models.Model):

    Address = models.CharField(max_length=300)

    Country = models.CharField(max_length=20)

    State = models.CharField(max_length=100)

    City = models.CharField(max_length=50)

    Postalcode = models.CharField(max_length=10)

    Addresstype = models.CharField(max_length=50)

    Additionalinfo = models.TextField()

    member = models.ForeignKey(MemberData, on_delete=models.CASCADE)






class MemberBusinessData(models.Model):

    Businessname = models.CharField(max_length=100)

    Businessdetails = models.TextField()

    Businessaddress = models.CharField(max_length=100)

    Businesscity = models.CharField(max_length=20)

    Businessemail = models.CharField(max_length=300)

    Businesspostalcode = models.CharField(max_length=100)

    member = models.ForeignKey(MemberData, on_delete=models.CASCADE)

