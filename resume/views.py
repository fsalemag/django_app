from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "resume/index.html")

def download(request):
    return render(request, "resume/index.html")