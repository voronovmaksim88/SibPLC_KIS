"""
URL configuration for SibPLC_KIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

# Это для аутентификации пользователя
from django.contrib.auth import views as auth_views

from SibPLC_KIS import settings
from main.views import index
from cost_calculation_automation_box.views import cost_calculation_automation_box
from serial_number.views import serial_number
from serial_number.views import form_add_box
from orders.views import get_orders
from orders.views import get_orders_as_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # маршрут до главной страницы
    path('cost_calculation_automation_box/', cost_calculation_automation_box),  #
    path('serial_number/', serial_number, name='serial_number'),
    path('get-orders-as-json/', get_orders_as_json, name='get-orders-as-json'),
    path('get_orders/', get_orders),
    path('form_add_box/', form_add_box, name='form_add_box'),
    # ... другие URL-шаблоны ...
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Если нужен logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
