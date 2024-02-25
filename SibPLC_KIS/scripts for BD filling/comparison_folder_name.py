# Переименовываем папку в соответствии с месяцем в БД
# Модуль os предоставляет множество функций для работы с операционной системой.
# Нам тут он нужен для создания папок
import os
import sqlite3
from pathlib import Path  # для переименования папок
import colorama
from colorama import Fore

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)


def get_subdirectories(path):
    # функция возвращает списком имена всех папок находящихся внутри папки по заданному пути
    subdirectories_list = []  # измененное имя переменной
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirectories_list.append(entry.name)  # измененное имя переменной
    return subdirectories_list  # вернуть измененное имя переменной


# Укажите путь к папке, в которой вы хотите найти подпапки
folder_path = "D:/YandexDisk/Труд/0_В работе/"

year = 2023

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
    print("sqlite3_order_list", sqlite3_order_list)
    print('')

# Получите имена всех подпапок
subdirectories = get_subdirectories(folder_path)

max_name_len = 0
for subdirectory in subdirectories:
    if len(subdirectory) > max_name_len:
        max_name_len = len(subdirectory)

# Выведите имена подпапок
space = ""
for subdirectory in subdirectories:
    space = " " * (max_name_len - len(subdirectory))
    print(subdirectory, end=space)
    num = subdirectory[0:3]
    # print('номер', num, end="   ")
    month = subdirectory[4:6]
    # print('месяц', month, end="   ")
    year = subdirectory[7:11]
    # print('год', year, end="   ")

    order = f"{num}-{month}-{year}"
    # print('заказ', order)

    index = subdirectory.index("_")
    name = subdirectory[index + 1:]
    # print('Имя заказа:', name)
    priority = 10
    status = 4
    serial = order

    if serial in sqlite3_order_list:
        print(Fore.GREEN + 'the order ' + serial + ' is in the database')
    else:
        print(Fore.RED + 'the order ' + serial + ' is NOT in the database')
    # print('')

    # if serial not in sqlite3_order_list:
    #     with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
    #         sqlite_cursor = connect.cursor()
    #         sqlite_cursor.execute("INSERT INTO main_order (serial, priority, status, name) VALUES (?, ?, ?, ?)",
    #                               (serial, priority, status, name))
    #     sqlite_cursor.close()
    #
    #     # Путь к текущей папке, которую нужно переименовать
    #     current_folder = Path(folder_path + '/' + subdirectory)
    #     print("текущий путь", current_folder)
    #
    #     # Новый путь с новым именем папки
    #     new_folder = Path(folder_path + '/' + new_name)
    #     print("новый путь  ", new_folder)
    #     print('')

    # try:
    #     current_folder.rename(new_folder)
    #     print(f"Папка '{current_folder}' переименована в '{new_folder}'")
    # except OSError as error:
    #     print(f"Ошибка: {error}")

    # if serial not in sqlite3_order_list:
    #     with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
    #         sqlite_cursor = connect.cursor()
    #         sqlite_cursor.execute("INSERT INTO main_order (serial, priority, status, name) VALUES (?, ?, ?, ?)",
    #                               (serial, priority, status, name))
    #     sqlite_cursor.close()
