#  from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
from django.contrib.auth.decorators import login_required


@login_required
def cost_calculation_automation_box(request):
    name = "Страница расчёта стоимости шкафа"
    countries = Countries.objects.all()
    print(countries)
    manufacturers = Manufacturers.objects.all()
    print(manufacturers)
    first_manufacturer = manufacturers.all()[0]
    country = Countries.objects.all()[first_manufacturer.country_id - 1]
    print(first_manufacturer.id, first_manufacturer.name, country.name)
    equipment_type = EquipmentType.objects.all()
    print(equipment_type)
    money = Money.objects.all()
    equipment = Equipment.objects.all()
    print(equipment)
    box_material = BoxMaterial.objects.all()
    print(box_material)
    box = Box.objects.all()
    print(box)

    return render(request, 'cost_calculation_automation_box.html',
                  {'name': name, 'countries': countries, 'manufacturers': manufacturers,
                   'equipment_type': equipment_type, 'money': money, 'equipment': equipment,
                   'box_material': box_material, 'box': box
                   })
