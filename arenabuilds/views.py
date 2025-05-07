from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render

from arenabuilds.forms import CreateBuildForm, LoginForm, RegisterForm, SearchForm
from arenabuilds.models import Build, Champion


def home(request):
    builds = Build.objects.all()
    champions = Champion.objects.all()

    return render(request, "home.html", {"builds": builds, "champions": champions})


# Vuln 1: A01:2021 Broken Access Control: Create page is accessible to everyone
# Fix 1: check if user is logged in
# @login_required
def create(request):
    if request.method == "POST":
        form = CreateBuildForm(request.POST)
        if form.is_valid():
            build = form.save(user=request.user)
            messages.info(request, f"Build created: {build.title}")
            return redirect("/")
    else:
        form = CreateBuildForm()

    return render(request, "create.html", {"form": form})


def search(request):
    form = SearchForm(request.GET)
    builds = Build.objects.none()

    if form.is_valid():
        query = form.cleaned_data.get("query")

        builds = Build.objects.all()
        if query:
            # Vuln 2: A03:2021: SQL Injection: Using raw SQL
            builds = list(
                Build.objects.raw(
                    f"SELECT * FROM arenabuilds_build WHERE title LIKE '%{query}%'",
                )
            )

            # Fix 2: use Django models instead of raw SQL
            # builds = builds.filter(
            #     Q(title__icontains=query)
            #     | Q(author__username__icontains=query)
            #     | Q(champion__name__icontains=query)
            # )

    return render(request, "search.html", {"form": form, "builds": builds})


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Vuln 4: A09:2021: Security Logging Failure: Not logging login attempts
            user = authenticate(username=username, password=password)
            if user is not None:
                # Fix 4: Log all login attempts
                # LoginLog.objects.create(
                #     username=username,
                #     ip_address=request.META.get("REMOTE_ADDR"),
                #     success=True,
                # )
                login(request, user)
                return redirect("/")

            # Fix 4: Log all login attempts
            # LoginLog.objects.create(
            #     username=username,
            #     ip_address=request.META.get("REMOTE_ADDR"),
            #     success=False,
            # )
            messages.error(request, "Invalid username or password")
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
            messages.error(request, "Failed to create user")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
