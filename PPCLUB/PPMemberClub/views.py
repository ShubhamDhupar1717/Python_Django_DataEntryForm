from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateMemberData, UpdateMemberData
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import MemberData, MemberFamilyData, MemberAddressData, MemberBusinessData

from django.contrib import messages
# Create your views here.

def Home(request):
    #return HttpResponse('Hey there...')
    return render(request, 'PPMemberClub/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'PPMemberClub/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")    

    context = {'form':form}

    return render(request, 'PPMemberClub/my-login.html', context=context)



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")




# - User Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = MemberData.objects.all()

    context = {'records': my_records}

    return render(request, 'PPMemberClub/dashboard.html', context=context)



# - Add new member data

@login_required(login_url='my-login')
def create_member(request):

    form = CreateMemberData()

    if request.method == "POST":

        form = CreateMemberData(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/create-member.html', context=context)




# - Update existing member data



# - Member Family details

@login_required(login_url='my-login')
def member_familydetail(request):

    member = MemberData.objects.all()
    my_records = member.member_id.all()

    context = {'record': my_records}

    return render(request, 'PPMemberClub/view-memberfamily.html', context=context)




