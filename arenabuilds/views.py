from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import redirect, render

from arenabuilds.forms import CreateBuildForm, LoginForm, RegisterForm
from arenabuilds.models import Build, Champion


def home(request):
    builds = Build.objects.all()
    champions = Champion.objects.all()

    return render(request, "home.html", {"builds": builds, "champions": champions})


# Fix 1: check if user is logged in
# @login_required
def create(request):
    if request.method == "POST":
        form = CreateBuildForm(request.POST)
        if form.is_valid():
            build = form.save(user=request.user)
            messages.Info(request, f"Build created: {build.title}")
            return redirect("/")
        else:
            messages.Error(request, "Failed to create build")
    else:
        form = CreateBuildForm()

    return render(request, "create.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
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


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect("/")
        else:
            messages.Error(request, "Failed to create user")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
