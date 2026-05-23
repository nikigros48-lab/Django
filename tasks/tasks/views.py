from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
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
    list_tasks = Task.objects.order_by("priority")
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
    

def get_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    return render(request, "tasks/task_info.html", context={"task": task})


def tasks_long(request:HttpRequest):
    list_tasks = Task.objects.all()
    longest_task = max(list_tasks, key=lambda task: len(task.title))
    return HttpResponse(f"{longest_task.title} - самая длинная задача!")


def completed_tasks(request:HttpRequest):
    list_tasks = Task.objects.all()
    completed = [task for task in list_tasks if task.completed]
    return HttpResponse(f"Завершенные задачи: {', '.join(task.title for task in completed)}")


def not_done_tasks(request:HttpRequest):
    list_tasks = Task.objects.all()
    not_done = [task for task in list_tasks if not task.completed]
    return HttpResponse(f"Незавершенные задачи: {', '.join(task.title for task in not_done)}")


def create_task(request:HttpRequest):
    error = None
    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority", 1)
        if title:
            Task.objects.create(title=title, priority=priority)
            return redirect("/tasks/")
        else:
            error = "Название задачи не может быть пустым!"
    return render(request, "tasks/tasks_create.html", context={"error": error})


def delete_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect("/tasks/")
    return render(request, "tasks/task_delete.html", context={"task": task})


def complete_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    task.completed = True
    task.save()
    return redirect(f"/tasks/{id}/")