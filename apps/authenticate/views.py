from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UserCreateForm


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


def login_view(request):
    return render(request, "pages/page-login.html")