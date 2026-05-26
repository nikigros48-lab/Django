from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task



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
        priority = request.POST.get("priority")
        if priority is None or priority == '':
            priority = 1
        else:
            priority = int(priority)
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


def delete_completed_tasks(request:HttpRequest):
    list_completed = Task.objects.filter(completed=True)
    if list_completed:
        list_completed.delete()
    return redirect("/tasks/")


def switch_status_task(request:HttpRequest, id:int):
    task = get_object_or_404(Task, id=id)
    if task.completed:
        task.completed = False
    else:
        task.completed = True
    task.save()
    return redirect(f"/tasks/{id}/")


def statistics(request:HttpRequest):
    list_tasks = Task.objects.all()
    total_tasks = len(list_tasks)
    len_completed = len([task for task in list_tasks if task.completed])
    len_not_completed = total_tasks - len_completed
    response = [f"Всего задач: {total_tasks}", f"Завершенных: {len_completed}", f"Незавершенных: {len_not_completed}"]
    return HttpResponse("<br>".join(response))


