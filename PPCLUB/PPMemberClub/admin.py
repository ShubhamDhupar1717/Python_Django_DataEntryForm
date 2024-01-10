from django.contrib import admin
from .models import MemberData, MemberAddressData, MemberBusinessData, MemberFamilyData

# Register your models here.
admin.site.register(MemberData)
admin.site.register(MemberAddressData)
admin.site.register(MemberBusinessData)
admin.site.register(MemberFamilyData)
