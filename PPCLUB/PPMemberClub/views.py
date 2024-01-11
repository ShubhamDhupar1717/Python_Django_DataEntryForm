from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateMemberData, UpdateMemberData, CreateMemberFamilyData, UpdateMemberFamilyData
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





#- View Memberdata

@login_required(login_url='my-login')
def view_member(request, pk):

    my_records = MemberData.objects.get(id=pk)

    context = {'form' : my_records}

    return render(request, 'PPMemberClub/view-member.html', context=context)




# - Create new member data

@login_required(login_url='my-login')
def create_member(request):

    form = CreateMemberData()

    if request.method == "POST":

        form = CreateMemberData(request.POST, request.FILES)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/create-member.html', context=context)




# - Update existing member data

@login_required(login_url='my-login')
def update_member(request, pk):

    record = MemberData.objects.get(id=pk)

    form = UpdateMemberData(instance=record)

    if request.method == "POST":

        form = UpdateMemberData(request.POST, instance=record)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/update-member.html', context=context)




# - Delete a record

@login_required(login_url='my-login')
def delete_member(request, pk):

    record = MemberData.objects.get(id=pk)

    record.delete()

    return redirect("dashboard")



# - View Member-Family details

@login_required(login_url='my-login')
def view_memberfamily(request, pk):

    my_records = MemberFamilyData.objects.get(member_id=pk)

    if my_records:
        context = {'record': my_records}
        return render(request, 'PPMemberClub/view-memberfamily.html', context=context)
    else:
        return redirect('create-memberfamily', pk=pk)





# Create Member-Family Details

@login_required(login_url='my-login')
def create_memberfamily(request):

    form = CreateMemberFamilyData()

    if request.method == "POST":

        form = CreateMemberFamilyData(request.POST)

        if form.is_valid():
            
            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/create-memberfamily.html', context=context)





# - Update existing member family data

@login_required(login_url='my-login')
def update_memberfamily(request, pk):

    record = MemberFamilyData.objects.get(id=pk)

    form = UpdateMemberFamilyData(instance=record)

    if request.method == "POST":

        form = UpdateMemberFamilyData(request.POST, instance=record)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/update-memberfamily.html', context=context)





# - View Member-Address details

@login_required(login_url='my-login')
def view_memberAddress(request, pk):

    my_records = MemberAddressData.objects.get(member_id=pk)

    if my_records:
        context = {'record': my_records}
        return render(request, 'PPMemberClub/view-memberaddress.html', context=context)







# - View Member-Business details

@login_required(login_url='my-login')
def view_memberBusiness(request, pk):

    my_records = MemberBusinessData.objects.get(member_id=pk)

    if my_records:
        context = {'record': my_records}
        return render(request, 'PPMemberClub/view-memberbusiness.html', context=context)
    

