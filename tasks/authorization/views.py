from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("task_list")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        super().form_valid(form)