from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateMemberData, UpdateMemberData, CreateMemberFamilyData, UpdateMemberFamilyData, CreateMemberAddressData, UpdateMemberAddressData, CreateMemberBusinessData, UpdateMemberBusinessData
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import MemberData, MemberFamilyData, MemberAddressData, MemberBusinessData
from django.contrib import messages
from .decorator import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


def Home(request):
    #return HttpResponse('Hey there...')
    return render(request, 'PPMemberClub/index.html')


#############################################################################################################################################################################################

# - Register a user
@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='NormalUsers')
            user.groups.add(group)
            
            messages.success(request, 'Account created successfully! Welcome ' + username)

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'PPMemberClub/register.html', context=context)


# - Login a user
@unauthenticated_user
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
                messages.success(request, 'Successfully Logged in!!')
                return redirect("dashboard")    

    context = {'form':form}

    return render(request, 'PPMemberClub/my-login.html', context=context)



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout successfully!")

    return redirect("my-login")




# - User Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = MemberData.objects.all()

    context = {'records': my_records}

    return render(request, 'PPMemberClub/dashboard.html', context=context)


#############################################################################################################################################################################################


#- View Memberdata

@login_required(login_url='my-login')
def view_member(request, pk):

    my_records = MemberData.objects.get(id=pk)

    context = {'form' : my_records}

    return render(request, 'PPMemberClub/view-member.html', context=context)



# - Create new member data

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def create_member(request):

    form1 = CreateMemberData()
    form2 = CreateMemberFamilyData()
    form3 = CreateMemberAddressData()
    form4 = CreateMemberBusinessData()
    if request.method == "POST":

        form1 = CreateMemberData(request.POST, request.FILES)
        form2 = CreateMemberFamilyData(request.POST)
        form3 = CreateMemberAddressData(request.POST)
        form4 = CreateMemberBusinessData(request.POST)

        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            member = form1.save()

            form2.instance.member_id = member.id
            form2.save()

            form3.instance.member_id = member.id
            form3.save()

            form4.instance.member_id = member.id
            form4.save()  

            messages.success(request, "Your record was created!")
            
            return redirect('dashboard')
        
        else:
            print(form1.errors)

        

    context = {'mform' : form1, 'mfform' : form2, 'maform' : form3, 'mbform' : form4}

    return render(request, 'PPMemberClub/create-member.html', context=context)



# - Update existing member data

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
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
@allowed_users(allowed_roles=['SuperUsers'])
def delete_member(request, pk):

    record = MemberData.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")


#############################################################################################################################################################################################



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
@allowed_users(allowed_roles=['SuperUsers'])
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



#############################################################################################################################################################################################



# - View Member-Address details

@login_required(login_url='my-login')
def view_memberaddress(request, pk):

    my_records = MemberAddressData.objects.get(member_id=pk)

    if my_records:
        context = {'record': my_records}
        return render(request, 'PPMemberClub/view-memberaddress.html', context=context)
    


# Create Member-Address Details

@login_required(login_url='my-login')
def create_memberaddress(request):

    form = CreateMemberAddressData()

    if request.method == "POST":

        form = CreateMemberAddressData(request.POST)

        if form.is_valid():
            
            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/create-memberaddress.html', context=context)



# - Update existing member family data

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def update_memberaddress(request, pk):

    record = MemberAddressData.objects.get(id=pk)

    form = UpdateMemberAddressData(instance=record)

    if request.method == "POST":

        form = UpdateMemberAddressData(request.POST, instance=record)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/update-memberaddress.html', context=context)



#############################################################################################################################################################################################



# - View Member-Business details

@login_required(login_url='my-login')
def view_memberbusiness(request, pk):

    my_records = MemberBusinessData.objects.get(member_id=pk)

    if my_records:
        context = {'record': my_records}
        return render(request, 'PPMemberClub/view-memberbusiness.html', context=context)
    


# Create Member-Address Details

@login_required(login_url='my-login')
def create_memberbusiness(request):

    form = CreateMemberBusinessData()

    if request.method == "POST":

        form = CreateMemberBusinessData(request.POST)

        if form.is_valid():
            
            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/create-memberbusiness.html', context=context)



# - Update existing member family data

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def update_memberbusiness(request, pk):

    record = MemberBusinessData.objects.get(id=pk)

    form = UpdateMemberBusinessData(instance=record)

    if request.method == "POST":

        form = UpdateMemberBusinessData(request.POST, instance=record)

        if form.is_valid():

            form.save()
            
            return redirect("dashboard")
        
        else:

            print(form.errors)

    context = {'form' : form}

    return render(request, 'PPMemberClub/update-memberbusiness.html', context=context)

    

#############################################################################################################################################################################################
