from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserCreatingForm, UserLoginForm
from django.views.generic import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout as auth_logout



def index(request):
    return render(request, 'index.html')


class Register(generic.CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreatingForm
    success_url = reverse_lazy('login')


class Login(FormView):
    template_name = 'blog/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super(Login, self).form_valid(form)
        else:
            form.add_error('username', 'Неправильное имя пользователя или пароль')
            return super(Login, self).form_valid(form)


def custom_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('index')
    else:
        return redirect('login')