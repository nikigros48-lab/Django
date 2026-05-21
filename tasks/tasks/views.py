from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Task

tasks_list = [
    {"title": "Купить молоко", "completed": True},
    {"title": "Позвонить маме", "completed": False},
    {"title": "Сделать домашнее задание", "completed": True},
    {"title": "Пойти в спортзал", "completed": False},
]


def home_page(request:HttpRequest):
    return render(request, "tasks/home.html", context={"title": "task managere",
                                                       "description": "Это домашняя страница нашего сайта!"})


def tasks(request:HttpRequest):
    list_tasks = Task.objects.all()
    return render(request, "tasks/tasks.html", context={"tasks": list_tasks})


def about(request:HttpRequest):
    return render(request, "tasks/about.html")


def user_detail(request:HttpRequest, id:int):
    return HttpResponse(f"user - {id}")


def contacts(request:HttpRequest):
    return render(request, "tasks/contacts.html")


def hello(request:HttpRequest, name:str):
    return HttpResponse(f"<h2>Привет, {name}!</h2>")


def number(request:HttpRequest, num:int):
    if num % 2 == 0:
        return HttpResponse(f"<h2>Число - {num} - четное!</h2>")
    return HttpResponse(f"<h2>Число - {num} - нечетное!</h2>")


def sum(request:HttpRequest, num1:int, num2:int):
    return HttpResponse(f"<h2>Сумма = {num1 + num2}!</h2>")


def maximum(request:HttpRequest, num1:int, num2:int):
    return HttpResponse(f"<h2>Максимальное число = {max(num1, num2)}!</h2>")
    

def get_task(request:HttpRequest, index:int):
    if index < 0 or index > 3:
        return HttpResponse("<h2>Задача не найдена!</h2>")
    return HttpResponse(f"<h2>Задача - {tasks_list[index]}!</h2>")

def tasks_long(request:HttpRequest):
    longest_task = max(tasks_list, key=lambda task: len(task["title"]))
    return HttpResponse(f"{longest_task['title']} - самая длинная задача!")

