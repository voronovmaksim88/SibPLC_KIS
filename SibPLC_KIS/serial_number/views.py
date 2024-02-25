from django.shortcuts import render, redirect
from main.models import *
from django.http import JsonResponse  # Для передачи данных в формате JSON
from .forms import AddBoxForm
from django.contrib.auth.decorators import login_required, permission_required

import colorama
from colorama import Fore

colorama.init(autoreset=True)


@login_required
def serial_number(request):
    print(Fore.GREEN + "привет из def serial_number(request):")
    form = AddBoxForm()
    name = "Учёт шкафов"
    box_accounting = Box_Accounting.objects.all().order_by('-serial_num')

    dict_models = {'name': name, 'box_accounting': box_accounting, 'form': form}
    return render(request, 'serial_number.html', dict_models)


def get_serial_number_json(request):
    print("печатаем request просто так,  чтоб он не серел", request)
    box_accounting = Box_Accounting.objects.all()
    data = list(box_accounting.values())  # Преобразует QuerySet в список словарей
    return JsonResponse(data, safe=False)  # Отправляет данные в формате JSON


@permission_required('main.app_name.can_add_box_accounting', raise_exception=True)
# Используем декоратор который разрешает вносить данные в таблицу учёта только тем пользователям,
# у которых есть на это право
def form_add_box(request):
    if request.method == 'POST':
        form = AddBoxForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('serial_number')  # Перенаправление на страницу успеха после сохранения
    else:
        form = AddBoxForm()
    return render(request, 'serial_number.html', {'form': form})
