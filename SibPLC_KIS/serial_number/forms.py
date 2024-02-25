from django import forms
from main.models import Box_Accounting
from main.models import Person
from main.models import Order
from django.db.models import Max

import colorama
from colorama import Fore

colorama.init(autoreset=True)


class AddBoxForm(forms.ModelForm):
    # Инициализация colorama для перехвата символов цвета в Windows
    print(Fore.GREEN + "привет из класса создания формы")

    class Meta:
        model = Box_Accounting
        fields = '__all__'

    def __init__(self, *args, **kwargs):  # чёрная магия, переопределяем инициализацию формы
        super(AddBoxForm, self).__init__(*args, **kwargs)
        # Получение максимального значения serial_num из уже существующих записей
        # и установка начального значения для новой формы.
        # Шаг 2: Выполняем агрегацию для получения максимального значения поля serial_num среди
        # всех записей в Box_Accounting
        aggregated_data = Box_Accounting.objects.aggregate(max_serial_number=Max('serial_num'))

        # Шаг 3: Из результата агрегации извлекаем значение максимального номера serial_num
        max_serial_num = aggregated_data['max_serial_number']

        # Если нет записей, max_serial_num будет None, в таком случае используем 0
        initial_serial_num = (max_serial_num or 0) + 1

        # Установка начального значения для поля serial_num в форме
        self.fields['serial_num'].initial = initial_serial_num
        self.fields['serial_num'].disabled = True  # запрет изменения

        # Устанавливаем queryset для поля scheme_developer, чтобы включить только сотрудников компании "СИБПЛК"
        person_sibplc = Person.objects.filter(company__name="СИБПЛК").order_by('surname')
        self.fields['scheme_developer'].queryset = person_sibplc
        self.fields['assembler'].queryset = person_sibplc
        self.fields['programmer'].queryset = person_sibplc
        self.fields['tester'].queryset = person_sibplc

        # Устанавливаем queryset для поля order, чтобы отображались только заявки которые ещё в работе
        order_in_work = Order.objects.filter(status=2).order_by('serial')
        self.fields['order'].queryset = order_in_work

        # Устанавливаем, что поле programmer не является обязательным к заполнению
        self.fields['programmer'].required = False
