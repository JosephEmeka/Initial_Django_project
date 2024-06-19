from django.shortcuts import render, HttpResponse


# Create your views here.

def welcome(request, name):
    return render(request, "index.html", {"name": ""})


def say_hello(request):
    return HttpResponse("welcome")
