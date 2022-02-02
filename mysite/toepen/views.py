from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# def index(request):
#     return HttpResponse("Hello, world. You're at the toepen index.")

def index(request):
    return render(request, 'toepen/index.html', {})

