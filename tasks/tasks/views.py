from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm



def home_page(request:HttpRequest):
    return render(request, "tasks/home.html", context={"title": "task managere",
                                                       "description": "Это домашняя страница нашего сайта!"})


def about(request:HttpRequest):
    return render(request, "tasks/about.html")


def contacts(request:HttpRequest):
    return render(request, "tasks/contacts.html")


def tasks(request:HttpRequest):
    list_tasks = Task.objects.order_by("priority")
    return render(request, "tasks/tasks.html", context={"tasks": list_tasks})


def get_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    return render(request, "tasks/task_info.html", context={"task": task})


def search_tasks(request:HttpRequest, word:str):
    list_tasks = Task.objects.filter(title__icontains=word)
    return HttpResponse(f"Задачи, содержащие '{word}':<br> {'<br>'.join({task.title for task in list_tasks})}")


def longest_task(request:HttpRequest):
    list_tasks = Task.objects.all()
    longest_task = max(list_tasks, key=lambda task: len(task.title))
    return HttpResponse(f"{longest_task.title} - самая длинная задача!")


def completed_tasks(request:HttpRequest):
    list_completed = Task.objects.filter(completed=True)
    return HttpResponse(f"Завершенные задачи:<br> {"<br>".join(task.title for task in list_completed)}")


def not_completed_tasks(request:HttpRequest):
    list_tasks = Task.objects.all()
    not_completed = [task for task in list_tasks if not task.completed]
    return HttpResponse(f"Незавершенные задачи:<br> {"<br>".join(task.title for task in not_completed)}")


def create_task(request:HttpRequest):
    error = None
    if request.method == "POST":
        title = request.POST.get("title")
        priority = int(request.POST.get("priority", 1))
        if title:
            Task.objects.create(title=title, priority=priority)
            return redirect("/tasks/")
        else:
            error = "Название задачи не может быть пустым!"
    return render(request, "tasks/tasks_create.html", context={"error": error})


def edit_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data["title"]
            task.priority = form.cleaned_data["priority"]
            task.save()
            return redirect(f"/tasks/{id}/")
    else:
        form = TaskForm(initial={"title": task.title, "priority": task.priority})
    return render(request, "tasks/task_edit.html", context={"form": form})


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


def delete_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect("/tasks/")
    return render(request, "tasks/task_delete.html", context={"task": task})


def delete_completed_tasks(request:HttpRequest):
    list_completed = Task.objects.filter(completed=True)
    if list_completed:
        list_completed.delete()
    return redirect("/tasks/")


def switch_status_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    task.completed = not task.completed
    task.save()
    return redirect(f"/tasks/{id}/")


def statistics(request:HttpRequest):
    list_tasks = Task.objects.all()
    total_tasks = len(list_tasks)
    len_completed = len([task for task in list_tasks if task.completed])
    len_not_completed = total_tasks - len_completed
    return HttpResponse("<br>".join([f"Всего задач: {total_tasks}", f"Завершенных: {len_completed}", f"Незавершенных: {len_not_completed}"]))


