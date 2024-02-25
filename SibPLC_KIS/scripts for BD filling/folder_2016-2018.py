# Скрипт для переименования папок по стандарту
# Модуль os предоставляет множество функций для работы с операционной системой.
# Нам тут он нужен для создания папок
import os
import sqlite3
from pathlib import Path  # для переименования папок


def get_subdirectories(path):
    subdirectories_list = []  # измененное имя переменной
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirectories_list.append(entry.name)  # измененное имя переменной
    return subdirectories_list  # вернуть измененное имя переменной


# Укажите путь к папке, в которой вы хотите найти подпапки
folder_path = "D:/YandexDisk/Труд/0_В работе/"

year = 2018
folder_path += str(year)

"""Копирование номеров заказов"""
with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
    cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
    cursor.execute("SELECT serial FROM main_order")

    all_row = cursor.fetchall()

    sqlite3_order_list = list()
    for row in all_row:
        # print(row[0])
        sqlite3_order_list.append(row[0])
    print(len(sqlite3_order_list), "заказов в БД sqlite3")
    # print("sqlite3_order_list", sqlite3_order_list)

# Получите имена всех подпапок
subdirectories = get_subdirectories(folder_path)

# Выведите имена подпапок
if year == 2016 or year == 2017 or year == 2018:
    for subdirectory in subdirectories:
        print(subdirectory)
        year = subdirectory[0:4]
        print('год', year)
        month = subdirectory[5:7]
        print('месяц', month)
        num = subdirectory[8:11]
        print('номер', num)

        order = f"{num}-{month}-{year}"
        print('заказ', order)

        index = subdirectory.index("_")
        name = subdirectory[index + 1:]
        print(name)
        new_name = order + "_" + name
        print(new_name)
        priority = 10
        status = 4
        serial = order

        # Путь к текущей папке, которую нужно переименовать
        current_folder = Path(folder_path + '/' + subdirectory)
        print("текущий путь", current_folder)

        # Новый путь с новым именем папки
        new_folder = Path(folder_path + '/' + new_name)
        print("новый путь  ", new_folder)
        print('')

        try:
            current_folder.rename(new_folder)
            print(f"Папка '{current_folder}' переименована в '{new_folder}'")
        except OSError as error:
            print(f"Ошибка: {error}")


