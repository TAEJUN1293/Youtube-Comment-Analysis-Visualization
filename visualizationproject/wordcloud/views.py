from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import render


@api_view(['GET'])
def trending(request):
    return HttpResponse("Hello, world.")


@api_view(['GET'])
def trending_detail(request):
    category = request.GET.get('category', None)
    context = {'category': category, 'videos': videos}
    return render(request, 'wordcloud/category_detail.html', context)