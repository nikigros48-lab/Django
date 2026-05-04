from django.http import HttpResponse, HttpRequest
from django.shortcuts import render



def home_page(request:HttpRequest):
    return HttpResponse("<h1>Привет</h1>")


def tasks(request:HttpRequest):
    return HttpResponse("<h2>Это список задач!</h2>")


def about(request:HttpRequest):
    return HttpResponse("<h2>Информация о нас!</h2>")


def user_detail(request:HttpRequest, id:int):
    return HttpResponse(f"user - {id}")