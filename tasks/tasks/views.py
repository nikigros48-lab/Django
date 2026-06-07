from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Task
from .forms import TaskForm



def home_page(request:HttpRequest):
    title = "Task Manager"
    description = "Это домашняя страница нашего сайта!"
    if request.user.is_authenticated:
        description += f" Привет, {request.user.username}!"
    else:
        description += " Пожалуйста, авторизуйтесь, чтобы управлять своими задачами."
        if request.method == "POST":
            if "login" in request.POST:
                return redirect("/login/")
            elif "register" in request.POST:
                return redirect("/register/")
    return render(request, "tasks/home.html", context={"title": title, "description": description,})


def about(request:HttpRequest):
    return render(request, "tasks/about.html")


def contacts(request:HttpRequest):
    return render(request, "tasks/contacts.html")


@login_required
def tasks(request:HttpRequest):
    list_tasks = Task.objects.filter(user=request.user).order_by("priority")
    return render(request, "tasks/tasks.html", context={"tasks": list_tasks})


@login_required
def get_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    return render(request, "tasks/task_info.html", context={"task": task})


@login_required
def search_task(request:HttpRequest, word:str):
    list_tasks = Task.objects.filter(title__icontains=word)
    return HttpResponse(f"Задачи, содержащие '{word}':<br> {'<br>'.join({task.title for task in list_tasks})}")


@login_required
def longest_task(request:HttpRequest):
    list_tasks = Task.objects.all()
    longest_task = max(list_tasks, key=lambda task: len(task.title))
    return HttpResponse(f"{longest_task.title} - самая длинная задача!")


@login_required
def completed_tasks(request:HttpRequest):
    list_completed = Task.objects.filter(completed=True)
    return HttpResponse(f"Завершенные задачи:<br> {"<br>".join(task.title for task in list_completed)}")


@login_required
def not_completed_tasks(request:HttpRequest):
    list_tasks = Task.objects.all()
    not_completed = [task for task in list_tasks if not task.completed]
    return HttpResponse(f"Незавершенные задачи:<br> {"<br>".join(task.title for task in not_completed)}")


@login_required
def create_task(request:HttpRequest):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return redirect("task_list")
    else:
            form = TaskForm()
    return render(request, "tasks/tasks_create.html", context={"form": form})


@login_required
def edit_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(f"/tasks/{id}/")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_edit.html", context={"form": form, "task": task})


@login_required
def search_tasks(request:HttpRequest):
    title = request.GET.get("title")
    priority = request.GET.get("priority")
    priority = int(priority) if priority else None
    tasks = Task.objects.all() if title or priority else []
    if title:
        tasks = tasks.filter(title__icontains=title)
    if priority:
        tasks = tasks.filter(priority=priority)
    return render(request, "tasks/search_task.html", context={"tasks": tasks, "word": title, "priority": priority})


@login_required
def delete_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect("/tasks/")
    return render(request, "tasks/task_delete.html", context={"task": task})


@login_required
def delete_completed_tasks(request:HttpRequest):
    list_completed = Task.objects.filter(completed=True)
    if list_completed:
        list_completed.delete()
    return redirect("/tasks/")


@login_required
def switch_status_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    task.completed = not task.completed
    task.save()
    return redirect(f"/tasks/{id}/")


@login_required
def statistics(request:HttpRequest):
    list_tasks = Task.objects.filter(user=request.user)
    total_tasks = len(list_tasks)
    len_completed = len([task for task in list_tasks if task.completed])
    len_not_completed = total_tasks - len_completed
    return HttpResponse("<br>".join([f"Всего задач: {total_tasks}", f"Завершенных: {len_completed}", f"Незавершенных: {len_not_completed}"]))


def login_view(request:HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", context={"form": form})


def logout_view(request:HttpRequest):
    logout(request)
    return redirect("/")

def register_view(request:HttpRequest):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})