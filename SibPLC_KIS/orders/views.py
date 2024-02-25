from django.shortcuts import render
from main.models import *
from django.http import JsonResponse  # Для передачи данных в формате JSON

from django.contrib.auth.decorators import login_required


@login_required
def get_orders(request):
    # sort_by = request.GET.get('sort', 'serial')  # 'serial_num' – поле сортировки по умолчанию
    name = "Заказы"
    # company = Company.objects.all()
    # person = Person.objects.all()

    # dict_models = {'name': name, 'company': company, 'person': person,}
    # dict_models = {'name': name}
    # return render(request, 'orders.html', dict_models)
    return render(request, 'orders.html', {'name': name, })


@login_required
def get_orders_as_json(request):
    print("печатаем request просто так,  чтоб он не серел", request)
    order = Order.objects.all()
    data = list(order.values())  # Преобразует QuerySet в список словарей
    return JsonResponse(data, safe=False)  # Отправляет данные в формате JSON
