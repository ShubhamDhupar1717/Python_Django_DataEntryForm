from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),

    #CRUD on Member
    path('dashboard', views.dashboard, name="dashboard"),
    path('create-member', views.create_member, name="create-member"),
    path('view-memberfamily', views.member_familydetail, name="view-memberfamily"),
]
