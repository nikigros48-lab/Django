from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, Category, Tag
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_info.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.object.tags.all()
        context["details"] = self.object.details
        return context
    
    def get_queryset(self):
        return self.model.objects.prefetch_related("tags").select_related("details").filter(user=self.request.user)

class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/tasks_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("task_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Task(user=self.request.user)
        return kwargs


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "tasks/task_edit.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("get_task", kwargs={"pk": self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        initial['description'] = self.object.details.description
        initial['estimated_hours'] = self.object.details.estimated_hours
        return initial


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("task_list")


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "tasks/categories.html"
    context_object_name = "categories"


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "tasks/category_info.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context["tasks"] = Task.objects.filter(category=category, user=self.request.user)
        return context


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "tasks/tag_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.object
        context["tasks"] = Task.objects.filter(tags=tag, user=self.request.user)
        return context


# def get_all_comments(request: HttpRequest, id: int) -> HttpResponse:
#     comments = Commentary.objects.filter(author=request.user)
#     pass


@login_required
def search_task(request:HttpRequest, word:str) -> HttpResponse:
    list_tasks = Task.objects.filter(title__icontains=word, user=request.user)
    return HttpResponse(f"Задачи, содержащие '{word}':<br> {('<br>'.join({task.title for task in list_tasks}))}")


@login_required
def completed_tasks(request:HttpRequest) -> HttpResponse:
    completed = Task.objects.filter(completed=True, user=request.user)
    return HttpResponse(f"Завершенные задачи:<br> {"<br>".join(task.title for task in completed)}")


@login_required
def not_completed_tasks(request:HttpRequest) -> HttpResponse:
    not_completed = Task.objects.filter(completed=False, user=request.user)
    return HttpResponse(f"Незавершенные задачи:<br> {"<br>".join(task.title for task in not_completed)}")


@login_required
def search_tasks(request:HttpRequest) -> HttpResponse:
    title = request.GET.get("title")
    priority = request.GET.get("priority")
    priority = int(priority) if priority else None
    tasks = Task.objects.filter(user=request.user) if title or priority else Task.objects.none()
    if title:
        tasks = tasks.filter(title__icontains=title)
    if priority:
        tasks = tasks.filter(priority=priority)
    return render(request, "tasks/search_task.html", context={"tasks": tasks, "word": title, "priority": priority})


@login_required
def delete_completed_tasks(request:HttpRequest) -> HttpResponse:
    list_completed = Task.objects.filter(completed=True, user=request.user)
    if list_completed:
        list_completed.delete()
    return redirect("task_list")


@login_required
def switch_status_task(request:HttpRequest, task_id:int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect("get_task", task.id)


@login_required
def statistics(request:HttpRequest) -> HttpResponse:
    list_tasks = Task.objects.filter(user=request.user)
    total_tasks = len(list_tasks)
    len_completed = len([task for task in list_tasks if task.completed])
    len_not_completed = total_tasks - len_completed
    return HttpResponse("<br>".join([f"Всего задач: {total_tasks}", f"Завершенных: {len_completed}", f"Незавершенных: {len_not_completed}"]))