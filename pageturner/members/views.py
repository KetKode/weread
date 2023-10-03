from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from boringavatars import avatar


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("welcome_page")
        else:
            messages.success(request, "There was an error logging in. Try again.")
            return redirect("login")
    else:

        return render(request, "authenticate/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('welcome_page')


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You are registered successfully.")
            return redirect("welcome_page")
    else:
        form = UserCreationForm()

    return render(request, "authenticate/register_user.html", {"form": form})


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)

    def generate_avatar(name, size=100, variant="beam", colors=None, title=False, square=False):
        if colors is None:
            colors = ["92A1C6", "146A7C", "F0AB3D", "C271B4", "C20D90"]

        avatar_svg = avatar(name, variant=variant, colors=colors, title=title, size=size, square=square)

        return avatar_svg

    for profile in profiles:
        profile.avatar_svg = generate_avatar(profile.user.username)

    return render(request, "profiles/profile_list.html", {"profiles": profiles})