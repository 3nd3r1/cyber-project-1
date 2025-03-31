from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.shortcuts import redirect, render

from arenabuilds.forms import LoginForm


def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        else:
            messages.Error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
