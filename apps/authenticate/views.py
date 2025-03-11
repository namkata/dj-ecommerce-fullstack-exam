from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView
)
from .forms import UserCreateForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST, request.FILES)  # Include files for profile picture
        if form.is_valid():
            form.save()  # Save the user
            return redirect("login")  # Redirect after successful registration
    else:
        form = UserCreateForm()

    return render(request, "pages/page-register.html", {"form": form})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirect if already logged in
    if request.method == "POST":
        print("Login successful")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Username: %s" % username)
        print("Password: %s" % password)
        # Authenticate the user using Django's authenticate function and login the user using Django's login function
        user = authenticate(request=request,username=username, password=password)
        print("Users", user)
        if user:
            login(request, user)  # Login the user
            return redirect("home")  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "pages/page-login.html")



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # Logout the user
    return redirect("home")  # Redirect after logout

# Add the following code in settings.py to redirect users to the login page after logout
# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'pages/password_reset.html'
    email_template_name = 'pages/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pages/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pages/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pages/password_reset_complete.html'

# Password Change Views
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'pages/password_change.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'pages/password_change_done.html'

# Profile Views
@login_required
def profile_view(request):
    return render(request, 'pages/page-account.html', {
        'user': request.user
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'pages/profile_edit.html', {
        'form': form
    })

# Create view functions to map class-based views to URLs
password_reset_view = CustomPasswordResetView.as_view()
password_reset_done_view = CustomPasswordResetDoneView.as_view()
password_reset_confirm_view = CustomPasswordResetConfirmView.as_view()
password_reset_complete_view = CustomPasswordResetCompleteView.as_view()
password_change_view = CustomPasswordChangeView.as_view()
password_change_done_view = CustomPasswordChangeDoneView.as_view()
