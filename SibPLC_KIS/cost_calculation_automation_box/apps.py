from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cost_calculation_automation_box'
    verbose_name = "Расчёт стоимости шкафа"