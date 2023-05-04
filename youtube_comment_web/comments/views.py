from .models import *
from django.shortcuts import render


def index(request):
    all_video = Video.objects.all()
    context = {'first_video': all_video[0].data}
    return render(request, 'comments/index.html', context)

def detail(request):
    all_video = Video.objects.all()
    context = {'first_video': all_video[0].data}
    return render(request, 'comments/detail.html', context)