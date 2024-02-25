from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Countries)
admin.site.register(EquipmentType)


class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "country")


class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', "name")


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
    'id', "name", "model", "vendore_code", "description", "type", "manufacturer", "price", "currency", "relevance",
    "price_date")


admin.site.register(Manufacturers, ManufacturersAdmin)
admin.site.register(Money, MoneyAdmin)
admin.site.register(Equipment, EquipmentAdmin)
