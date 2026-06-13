from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect




def home_page(request: HttpRequest) -> HttpResponse:
    title = "Task Manager"
    description = "Это домашняя страница нашего сайта!"
    if request.user.is_authenticated:
        description += f" Привет, {request.user.username}!"
    else:
        description += " Пожалуйста, авторизуйтесь, чтобы управлять своими задачами."
        if request.method == "POST":
            if "login" in request.POST:
                return redirect("login")
            elif "register" in request.POST:
                return redirect("register")
    return render(request, "info/home.html", context={"title": title, "description": description,})


def about(request:HttpRequest) -> HttpResponse:
    return render(request, "info/about.html")


def contacts(request:HttpRequest) -> HttpResponse:
    return render(request, "info/contacts.html")