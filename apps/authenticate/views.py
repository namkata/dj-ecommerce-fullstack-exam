from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UserCreateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
