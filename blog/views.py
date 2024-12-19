from msilib.schema import ListView
from django.shortcuts import render
from django.views import generic
from .models import Post


def index(request):
    return render(request, 'index.html')