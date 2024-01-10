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
    path('update-member', views.update_member, name="update-member"),
    
    #CRUD on MemberFamilyData
    path('view-memberfamily/<int:pk>', views.member_familydetail, name="view-memberfamily"),
]
