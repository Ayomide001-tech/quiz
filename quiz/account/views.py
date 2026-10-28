from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
# from unicodedata import category
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Account
from django.contrib import messages
from .forms import (
    registrationForm,
    loginAuthenticationForm,
    adminRegistrationForm,
    staffRegistrationForm,
    UserUpdateForm,
    AccountRoleForm,
)
from django.contrib.auth.decorators import login_required


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('superuserpage')
        elif request.user.is_admin:
            return redirect('adminpage')
        return redirect('dashboard')

    if request.method == 'POST':
        form = loginAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # Django's default authentication backend expects `username=` even when USERNAME_FIELD is email.
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('superuserpage')  # Redirect to admin page if user is superuser
                elif user.is_admin:
                    return redirect('adminpage')
                return redirect('dashboard')  # Redirect to a success page after login
            else:
                form.add_error(None, "Invalid login credentials")
            
    else:
        form = loginAuthenticationForm()

    return render(request, 'account/login.html', {'form': form})




def register(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = registrationForm()

    return render(request, 'account/register.html', {'form': form})



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')




def admin_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('homepage')

    if request.method == 'POST':
        form = adminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_admin:

                return redirect('adminpage')  # Redirect to admin page after successful registration
            return redirect('login')
    else:
        form = adminRegistrationForm()
    
    return render(request, 'superuser&admin/admin_form.html', {'form': form})



def view_all_user(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')  # Redirect to login if user is not authenticated or not superuser

    presentusers = Account.objects.all()
    return render(request, 'account/view_all_user.html', {'presentusers': presentusers})


@login_required(login_url='login')
@require_POST
def update_account_role(request, account_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers can change account roles.")

    account = get_object_or_404(Account, pk=account_id)
    form = AccountRoleForm(request.POST, account=account)
    if not form.is_valid():
        messages.error(request, "Choose a valid account role.")
        return redirect('view_all_user')

    if account.pk == request.user.pk and form.cleaned_data['role'] != 'superuser':
        messages.error(request, "You cannot remove your own superuser access.")
        return redirect('view_all_user')

    form.save()
    messages.success(request, f"Updated the role for {account.username}.")
    return redirect('view_all_user')



@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('dashboard')  # Redirect to the same page after successful update

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'account/edit_profile.html', {'form': form})
