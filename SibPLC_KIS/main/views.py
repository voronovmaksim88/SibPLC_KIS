from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    name = "Главная"
    return render(request, 'index.html', {'name': name, })
    # return render(request, "Hello ")
    # return HttpResponse(request, 'index.html')
    # return HttpResponse("Hello")
