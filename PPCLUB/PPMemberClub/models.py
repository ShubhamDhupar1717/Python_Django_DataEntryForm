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




class ProposedMemberData(models.Model):

     # these are the member data properties

    Fullname = models.CharField(max_length=100, null=True)

    Email = models.CharField(max_length=250, null=True)

    Dob = models.DateTimeField(null=True)

    Resphone = models.CharField(max_length=20, null=True)

    Altermobileno = models.CharField(max_length=20, null=True)

    Resaddress = models.CharField(max_length=300, null=True)

    Officeno = models.CharField(max_length=255, null=True)

    Country = models.CharField(max_length=125, null=True)

    Profilepic = models.ImageField(upload_to='pics', null=True)

    Signature = models.ImageField(upload_to='pics', null=True)

    
  # these are MemberFamilyData properties

    firstname = models.CharField(max_length=100, null=True)

    lastname = models.CharField(max_length=100, null=True)

    relation = models.CharField(max_length=100, null=True)

    contactno = models.CharField(max_length=20, null=True)

    homeaddress = models.CharField(max_length=300, null=True)

    Spousename = models.CharField(max_length=200, null=True)

    Spousedob = models.DateTimeField(null=True)

    Childname = models.CharField(max_length=100, null=True)


    # these are the MemberAddressData properties

    Address = models.CharField(max_length=300, null=True)

    Country = models.CharField(max_length=20, null=True)

    State = models.CharField(max_length=100, null=True)

    City = models.CharField(max_length=50, null=True)

    Postalcode = models.CharField(max_length=10, null=True)

    Addresstype = models.CharField(max_length=50, null=True)

    Additionalinfo = models.TextField(null=True)


    # these are the MemberBusinessData properties

    Businessname = models.CharField(max_length=100, null=True)

    Businessdetails = models.TextField(null=True)

    Businessaddress = models.CharField(max_length=100, null=True)

    Businesscity = models.CharField(max_length=20, null=True)

    Businessemail = models.CharField(max_length=300, null=True)

    Businesspostalcode = models.CharField(max_length=100, null=True)


    proposed_memberdata = models.OneToOneField(MemberData, on_delete=models.CASCADE, null=True, unique=True)
    proposed_memberfamilydata = models.OneToOneField(MemberFamilyData, on_delete=models.CASCADE, null=True, unique=True)
    proposed_memberaddressdata = models.OneToOneField(MemberAddressData, on_delete=models.CASCADE, null=True, unique=True)
    proposed_memberbusinessdata = models.OneToOneField(MemberBusinessData, on_delete=models.CASCADE, null=True, unique=True)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

