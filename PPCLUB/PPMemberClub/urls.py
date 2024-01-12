from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('dashboard', views.dashboard, name="dashboard"),

    #CRUD on Member
    path('view-member/<int:pk>', views.view_member, name="view-member"),
    path('create-member', views.create_member, name="create-member"),
    path('update-member/<int:pk>', views.update_member, name="update-member"),
    path('delete-member/<int:pk>', views.delete_member, name="delete-member"),

    #CRUD on MemberFamilyData
    path('view-memberfamily/<int:pk>', views.view_memberfamily, name="view-memberfamily"),
    path('create-memberfamily/<int:pk>', views.create_memberfamily, name="create-memberfamily"),
    path('update-memberfamily/<int:pk>', views.update_memberfamily, name="update-memberfamily"),

    #CRUD on MemberAddressData
    path('view-memberaddress/<int:pk>', views.view_memberaddress, name="view-memberaddress"),
    path('create-memberaddress/<int:pk>', views.create_memberaddress, name="create-memberaddress"),
    path('update-memberaddress/<int:pk>', views.update_memberaddress, name="update-memberaddress"),

    #CRUD on MemberBusinessData
    path('view-memberbusiness/<int:pk>', views.view_memberbusiness, name="view-memberbusiness"),
    path('create-memberbusiness/<int:pk>', views.create_memberbusiness, name="create-memberbusiness"),
    path('update-memberbusiness/<int:pk>', views.update_memberbusiness, name="update-memberbusiness"),
]
