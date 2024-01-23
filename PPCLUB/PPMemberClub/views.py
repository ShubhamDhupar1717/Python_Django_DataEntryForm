from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateMemberData, UpdateMemberData, CreateMemberFamilyData, UpdateMemberFamilyData, CreateMemberAddressData, UpdateMemberAddressData, CreateMemberBusinessData, UpdateMemberBusinessData, ProposedMemberDataForm, ProposedMemberFamilyDataForm, ProposedMemberAddressDataForm, ProposedMemberBusinessDataForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import MemberData, MemberFamilyData, MemberAddressData, MemberBusinessData, ProposedMemberData
from django.contrib import messages
from .decorator import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict


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
def update_member(request, pk):
    # Retrieve the existing member data
    record = MemberData.objects.get(id=pk)

    # Specify the fields you want to copy
    fields_to_copy = ['Fullname', 'Email', 'Dob', 'Resphone', 'Altermobileno', 'Resaddress', 'Officeno', 'Country', 'Profilepic', 'Signature']

    # Create a dictionary of field values from the original form
    form_data = {field: getattr(record, field) for field in fields_to_copy}

    # Initialize the original form for SuperUsers
    form = UpdateMemberData(request.POST or None, instance=record)

    # Initialize the proposed data form for FrontDesk users with the copied data
    form1 = ProposedMemberDataForm(request.POST or None, initial=form_data, instance=ProposedMemberData())

    if request.method == "POST":
        # Check if the user is a SuperUser
        if request.user.is_superuser:
            form = UpdateMemberData(request.POST, instance=record)
            if form.is_valid():
                # Save the data in the original MemberData table
                form.save()
                return redirect("dashboard")
            else:
                print(form.errors)

        # Check if the user is a FrontDesk user
        elif request.user.username == 'FrontDesk':
            # Save the data in the ProposedMemberData table
            if form1.is_valid():
                form1.instance.proposed_memberdata_id = record.id
                form1.save()
                return redirect("dashboard")
            else:
                print(form1.errors)

    # Render the appropriate form based on the user role
    context = {'form': form} if request.user.is_superuser else {'form': form1}
    return render(request, 'PPMemberClub/update-member.html', context=context)




# - FrontDesk User Update Permission / Proposed data ready to be Accept or Reject.

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def proposed_memberdata(request, pk):
    proposeddata = ProposedMemberData.objects.get(proposed_memberdata_id=pk)
    if not proposeddata :
        return redirect("dashboard")
    
    memberdata = MemberData.objects.get(id=pk)
    form = UpdateMemberData(request.POST or None, instance=memberdata)
    
    # Get the initial data for the proposed form
    form_data = model_to_dict(proposeddata)

    form1 = ProposedMemberDataForm(request.POST or None, instance=proposeddata)
    form2 = UpdateMemberData(request.POST or None, initial=form_data, instance=memberdata)

    # If the user clicks on Accept button, save the proposed data into the MemberData Table
    if request.method == 'POST':
        if form2.is_valid():
            form2.save()
            proposeddata.delete()
            return redirect("dashboard")


    context = {'form1': form1, 'form2': form}
    return render(request, 'PPMemberClub/proposedmemberdata.html', context)



# - Delete a Proposed Table record

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def delete_proposedmember(request, pk):

    proposeddata = ProposedMemberData.objects.get(id=pk)

    proposeddata.delete()

    messages.success(request, "Proposed data request was deleted!")

    return redirect("dashboard")



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
@allowed_users(allowed_roles=['SuperUsers'])
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

    # Specify the fields you want to copy
    fields_to_copy = ['firstname', 'lastname', 'relation', 'contactno', 'homeaddress', 'Spousename', 'Spousedob', 'Childname']

    # Create a dictionary of field values from the original form
    form_data = {field: getattr(record, field) for field in fields_to_copy}

    # Initialize the original form for SuperUsers
    form = UpdateMemberFamilyData(request.POST or None, instance=record)

    # Initialize the proposed data form for FrontDesk users with the copied data
    form1 = ProposedMemberFamilyDataForm(request.POST or None, initial=form_data, instance=ProposedMemberData())

    if request.method == "POST":
        # Check if the user is a SuperUser
        if request.user.is_superuser:
            form = UpdateMemberFamilyData(request.POST, instance=record)
            if form.is_valid():
                # Save the data in the original MemberData table
                form.save()
                return redirect("dashboard")
            else:
                print(form.errors)

        # Check if the user is a FrontDesk user
        elif request.user.username == 'FrontDesk':
            # Save the data in the ProposedMemberData table
            if form1.is_valid():
                form1.instance.proposed_memberfamilydata_id = record.id
                form1.save()
                return redirect("dashboard")
            else:
                print(form1.errors)

    # Render the appropriate form based on the user role
    context = {'form': form} if request.user.is_superuser else {'form': form1}

    return render(request, 'PPMemberClub/update-memberfamily.html', context=context)





    
# - FrontDesk User Update Permission / Proposed data ready to be Accept or Reject.

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def proposed_memberfamilydata(request, pk):
    proposeddata = ProposedMemberData.objects.get(proposed_memberfamilydata_id=pk)
    if not(proposeddata):
        return redirect("dashboard")
    memberfamilydata = MemberFamilyData.objects.get(id=pk)

    fields_to_copy = ['firstname', 'lastname', 'relation', 'contactno', 'homeaddress', 'Spousename', 'Spousedob', 'Childname']

    form_data = {field: getattr(proposeddata, field) for field in fields_to_copy}

    form1 = ProposedMemberFamilyDataForm(request.POST or None, instance=proposeddata)
    #form2 = UpdateMemberData(request.POST or None, instance=memberdata)
    form2 = UpdateMemberFamilyData(request.POST or None, initial=form_data, instance=memberfamilydata)

    # If the user clicks on Accept button, save the proposed data into the MemberData Table
    if request.method == 'POST':
        if form2.is_valid():
            form2.save()
            proposeddata.delete()
            return redirect("dashboard")


    context = {'form1': form1, 'form2': form2}
    return render(request, 'PPMemberClub/proposedmemberfamilydata.html', context)



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
@allowed_users(allowed_roles=['SuperUsers'])
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

def update_memberaddress(request, pk):

    record = MemberAddressData.objects.get(id=pk)

   # Specify the fields you want to copy
    fields_to_copy = ['Address', 'Country', 'State', 'City', 'Postalcode', 'Addresstype', 'Additionalinfo']

    # Create a dictionary of field values from the original form
    form_data = {field: getattr(record, field) for field in fields_to_copy}

    # Initialize the original form for SuperUsers
    form = UpdateMemberAddressData(request.POST or None, instance=record)

    # Initialize the proposed data form for FrontDesk users with the copied data
    form1 = ProposedMemberAddressDataForm(request.POST or None, initial=form_data, instance=ProposedMemberData())

    if request.method == "POST":
        # Check if the user is a SuperUser
        if request.user.is_superuser:
            form = UpdateMemberAddressData(request.POST, instance=record)
            if form.is_valid():
                # Save the data in the original MemberData table
                form.save()
                return redirect("dashboard")
            else:
                print(form.errors)

        # Check if the user is a FrontDesk user
        elif request.user.username == 'FrontDesk':
            # Save the data in the ProposedMemberData table
            if form1.is_valid():
                form1.instance.proposed_memberaddressdata_id = record.id
                form1.save()
                return redirect("dashboard")
            else:
                print(form1.errors)

    # Render the appropriate form based on the user role
    context = {'form': form} if request.user.is_superuser else {'form': form1}

    return render(request, 'PPMemberClub/update-memberaddress.html', context=context)




# - FrontDesk User Update Permission / Proposed data ready to be Accept or Reject.

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def proposed_memberaddressdata(request, pk):
    proposeddata = ProposedMemberData.objects.get(proposed_memberaddressdata_id=pk)
    if not(proposeddata):
        return redirect("dashboard")
    memberaddressdata = MemberAddressData.objects.get(id=pk)

    fields_to_copy = ['Address', 'Country', 'State', 'City', 'Postalcode', 'Addresstype', 'Additionalinfo']

    form_data = {field: getattr(proposeddata, field) for field in fields_to_copy}

    form1 = ProposedMemberAddressDataForm(request.POST or None, instance=proposeddata)
    #form2 = UpdateMemberData(request.POST or None, instance=memberdata)
    form2 = UpdateMemberAddressData(request.POST or None, initial=form_data, instance=memberaddressdata)

    # If the user clicks on Accept button, save the proposed data into the MemberData Table
    if request.method == 'POST':
        if form2.is_valid():
            form2.save()
            proposeddata.delete()
            return redirect("dashboard")


    context = {'form1': form1, 'form2': form2}
    return render(request, 'PPMemberClub/proposedmemberaddressdata.html', context)



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
@allowed_users(allowed_roles=['SuperUsers'])
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

def update_memberbusiness(request, pk):

    record = MemberBusinessData.objects.get(id=pk)

    # Specify the fields you want to copy
    fields_to_copy = ['Businessname', 'Businessdetails', 'Businessaddress', 'Businesscity', 'Businessemail', 'Businesspostalcode']

    # Create a dictionary of field values from the original form
    form_data = {field: getattr(record, field) for field in fields_to_copy}

    # Initialize the original form for SuperUsers
    form = UpdateMemberBusinessData(request.POST or None, instance=record)

    # Initialize the proposed data form for FrontDesk users with the copied data
    form1 = ProposedMemberBusinessDataForm(request.POST or None, initial=form_data, instance=ProposedMemberData())

    if request.method == "POST":
        # Check if the user is a SuperUser
        if request.user.is_superuser:
            form = UpdateMemberBusinessData(request.POST, instance=record)
            if form.is_valid():
                # Save the data in the original MemberData table
                form.save()
                return redirect("dashboard")
            else:
                print(form.errors)

        # Check if the user is a FrontDesk user
        elif request.user.username == 'FrontDesk':
            # Save the data in the ProposedMemberData table
            if form1.is_valid():
                form1.instance.proposed_memberbusinessdata_id = record.id
                form1.save()
                return redirect("dashboard")
            else:
                print(form1.errors)

    # Render the appropriate form based on the user role
    context = {'form': form} if request.user.is_superuser else {'form': form1}

    return render(request, 'PPMemberClub/update-memberbusiness.html', context=context)





# - FrontDesk User Update Permission / Proposed data ready to be Accept or Reject.

@login_required(login_url='my-login')
@allowed_users(allowed_roles=['SuperUsers'])
def proposed_memberbusinessdata(request, pk):
    proposeddata = ProposedMemberData.objects.get(proposed_memberbusinessdata_id=pk)
    if not(proposeddata):
        return redirect("dashboard")
    memberbusinessdata = MemberBusinessData.objects.get(id=pk)

    fields_to_copy = ['Businessname', 'Businessdetails', 'Businessaddress', 'Businesscity', 'Businessemail', 'Businesspostalcode']

    form_data = {field: getattr(proposeddata, field) for field in fields_to_copy}

    form1 = ProposedMemberBusinessDataForm(request.POST or None, instance=proposeddata)
    #form2 = UpdateMemberData(request.POST or None, instance=memberdata)
    form2 = UpdateMemberBusinessData(request.POST or None, initial=form_data, instance=memberbusinessdata)

    # If the user clicks on Accept button, save the proposed data into the MemberData Table
    if request.method == 'POST':
        if form2.is_valid():
            form2.save()
            proposeddata.delete()
            return redirect("dashboard")


    context = {'form1': form1, 'form2': form2}
    return render(request, 'PPMemberClub/proposedmemberbusinessdata.html', context)

    

#############################################################################################################################################################################################
