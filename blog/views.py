from msilib.schema import ListView
from django.shortcuts import render
from django.views import generic
from .models import Post
from .forms import UserCreatingForm


def index(request):
    return render(request, 'index.html')


class Register(generic.CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreatingForm