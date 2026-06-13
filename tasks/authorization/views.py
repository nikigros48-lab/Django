from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


def login_view(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", context={"form": form})


def logout_view(request:HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def register_view(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})