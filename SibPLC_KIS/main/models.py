from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Countries(models.Model):
    name = models.CharField(max_length=16)
    objects = models.Manager()

    class Meta:
        verbose_name = "Страны"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Manufacturers(models.Model):  # Класс "Производители", это не конкретное лицо это типа брэнд
    name = models.CharField(max_length=16)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


# Класс "Производители"
# name - имя производителя
# Country - страна производителя, каждому производителю соответствует только одна страна
# on_delete=models.SET_NULL, null=True - если вы удалите запись в модели `Countries`,
# поле `Country` во всех связанных записях модели `Manufacturers` будет установлено в `NULL`,
# а сами эти записи останутся нетронутыми.


# Класс "Типы оборудования"
class EquipmentType(models.Model):
    name = models.CharField(max_length=16)
    objects = models.Manager()

    def __str__(self):
        return self.name


# Класс "Деньги"
# тут просто имена валют
class Money(models.Model):
    name = models.CharField(max_length=8)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Equipment(models.Model):  # Класс "Оборудование"
    name = models.CharField(max_length=32)  # Имя
    model = models.CharField(max_length=32, blank=True, unique=True)  # Модель
    vendore_code = models.CharField(max_length=32, blank=True, unique=True)  # Артикул, код поставщика
    description = models.TextField(blank=True)  # Описание
    # Если поле имеет blank = True, проверка формы позволит ввести пустое значение. Если в поле есть blank = False,
    # поле будет обязательным
    type = models.ForeignKey(EquipmentType, on_delete=models.SET_NULL, null=True)  # Тип
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.SET_NULL, null=True)  # Производитель
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])  # Цена
    currency = models.ForeignKey(Money, on_delete=models.SET_NULL, null=True)  # Валюта
    relevance = models.BooleanField(default=True)  # Актуальность
    price_date = models.DateField()  # Дата обновления цены
    photo = models.ImageField(upload_to="photos", null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class BoxMaterial(models.Model):  # Материалы шкафов
    name = models.CharField(max_length=16)  # Имя
    objects = models.Manager()


class BoxIp(models.Model):  # Степень защиты корпусов
    name = models.CharField(max_length=16)  # Имя
    objects = models.Manager()


class Box(models.Model):  # Корпуса шкафов
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, primary_key=True)
    # связь с таблицей оборудования
    # on_delete = models.CASCADE говорит, что данные текущей модели(UserAccount) будут удаляться в случае удаления
    # связанного объекта главной модели(User).
    # primary_key = True указывает, что внешний ключ(через который идет связь с главной моделью) в то же
    # время будет выступать и в качестве первичного ключа. И создавать отдельное поле для первичного ключа не надо.
    material = models.ForeignKey(BoxMaterial, on_delete=models.SET_NULL, null=True)  # материал
    height = models.IntegerField()  # высота
    width = models.IntegerField()  # ширина
    depth = models.IntegerField()  # глубина
    ip = models.ForeignKey(BoxIp, on_delete=models.SET_NULL, null=True)  # степень защиты
    objects = models.Manager()


class City(models.Model):  # Города
    # The unique option in Django models is used to specify whether or not a field must be
    # unique across all objects in the database.
    name = models.CharField(max_length=32, unique=True)  # Имя
    objects = models.Manager()

    def __str__(self):
        return self.name


class CompaniesForm(models.Model):  # Формы компаний
    name = models.CharField(max_length=8)  # Имя
    objects = models.Manager()


class Company(models.Model):  # Компаний, юрлица, ИП, заказчики, поставщики
    form = models.ForeignKey(CompaniesForm, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, unique=True)  # Имя
    note = models.CharField(max_length=255, null=True)  # Примечание
    # Здесь устанавливаем связь с моделью Города
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='companies')
    objects = models.Manager()

    '''
    - ForeignKey указывает, что каждая запись в модели Company связана с одной записью в модели City.
    - Параметр on_delete=models.CASCADE означает, что когда вы удаляете город,
        все связанные с ним компании тоже будут удалены.
        Это поведение по умолчанию, но Django предоставляет и другие опции.
    - Параметр related_name='companies' предоставляет обратное имя для связи,
        чтобы вы могли получить доступ ко всем компаниям города.
        Например, если у вас есть объект City, вы можете использовать my_city.companies.all()
        для получения всех компаний в этом городе.
    '''

    def __str__(self):
        return self.name


class Person(models.Model):  # Люди
    name = models.CharField(max_length=32, null=True)  # Имя
    patronymic = models.CharField(max_length=32, null=True)  # Отчество
    surname = models.CharField(max_length=32, null=True)  # Фамилия
    phone = models.CharField(max_length=16, null=True)  # Телефон
    email = models.CharField(max_length=32, null=True)  # Почта
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)  # Компания
    objects = models.Manager()

    def __str__(self):
        return f"{self.surname} {self.name}"


class Order(models.Model):  # таблица заказов (заявок, проектов)
    name = models.CharField(max_length=64, null=True)  # Название, краткое описание, объект, что вообще от нас хотели
    serial = models.CharField(max_length=16, null=False, primary_key=True)
    # Серийный номер заказа, формат NNN-MM-YYYY
    # NNN - порядковый номер в этом году
    # MM - месяц создания
    # YYYY - год создания
    customer = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)  # Заказчик
    priority = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    # приоритет от 1 до 9, 1-самое важное, 9 самое НЕ важно.
    # Значение 10 будет означать что приоритета нет, в идеале нет приоритет а должно было быть None
    # Но сортировка тогда сильно усложнилась, поэтому я решил сделать по колхозному, но быстро и понятно
    status = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    """
    0 "Не определён"
    1 "На согласовании"
    2 = "В работе"
    3 = "Просрочено"
    4 = "Выполнено в срок"
    5 = "Выполнено НЕ в срок"
    6 = "Не согласовано"
    7 = "На паузе"
    else = "?"
    """
    objects = models.Manager()

    def __str__(self):
        return f"{self.serial}"


class Box_Accounting(models.Model):  # учёт шкафов
    serial_num = models.IntegerField(  # Серийный номер
        unique=True,
        primary_key=True,
        verbose_name="Серийный номер"
    )
    name = models.CharField(  # Название шкафа
        max_length=32,
        null=False,
        verbose_name="Название"
    )
    order = models.ForeignKey(  # Заказ(через него и заказчика найдём)
        Order, null=False,
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    scheme_developer = models.ForeignKey(  # Разработчик схемы
        Person,
        on_delete=models.CASCADE,
        null=False,
        related_name="developed_boxes",  # Уникальное имя 'related_name' для scheme_developer
        verbose_name="Разработчик схемы"
    )
    assembler = models.ForeignKey(  # Сборщик
        Person,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        null=False,
        related_name="assembled_boxes",  # Уникальное имя 'related_name' для assembler
        verbose_name="Сборщик"
    )
    programmer = models.ForeignKey(  # Программист
        Person,
        on_delete=models.SET_NULL,
        null=True,
        related_name="programmer_boxes",  # Уникальное имя 'related_name' для programmer
        verbose_name="Программист"
    )
    tester = models.ForeignKey(  # Тестировщик
        Person,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        null=False,
        related_name="tested_boxes",  # Уникальное имя 'related_name' для tester
        verbose_name="Тестировщик")

    objects = models.Manager()
    # тут иакой опасный момент, если удалить человека который участвовал в создании шкафа или компанию заказчика,
    # то это сразу удалит и запись из БД о серийном номере шкафа
    # остаются надеяться чтоб БД при этом сообщит об этом
    # Поэтому надо быть очень аккуратным при удалении информации из БД
    # Но зато БД не даст сделать запись с недостающей информацией

    '''  
    class Equipment_Suppliers(models.Model):  # Поставщик-Оборудование
        equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE)
        supplier = 
        - Supplier_ID(компания)
        - Price_in(наша  входная   цена)
        - Price_out(выходная   цена, розница)
        - Link(ссылка)
        
    
    '''
