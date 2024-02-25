# Модуль os предоставляет множество функций для работы с операционной системой.
# Нам тут он нужен для создания папок
import os
import sqlite3
import colorama
from colorama import Fore

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)



def get_subdirectories(path):
    subdirectories_list = []  # измененное имя переменной
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirectories_list.append(entry.name)  # измененное имя переменной
    return subdirectories_list  # вернуть измененное имя переменной


# Укажите путь к папке, в которой вы хотите найти подпапки
folder_path = "D:/YandexDisk/Труд/0_В работе/"

year = 2022
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
for subdirectory in subdirectories:
    print(subdirectory)
    year = subdirectory[7:11]
    print('год', year)
    month = subdirectory[4:6]
    print('месяц', month)
    num = subdirectory[0:3]
    num = "0" + num if len(num) == 2 else num
    print('номер', num)

    order = f"{num}-{month}-{year}"
    print('заказ', order)

    index = subdirectory.index("_")
    name = subdirectory[index + 1:]
    print(name)
    priority = 10
    status = 4
    serial = order

    if serial not in sqlite3_order_list:
        print(Fore.RED + "надо внести " + serial)
        with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
            sqlite_cursor = connect.cursor()
            sqlite_cursor.execute("INSERT INTO main_order (serial, priority, status, name) VALUES (?, ?, ?, ?)",
                                  (serial, priority, status, name))
        sqlite_cursor.close()

    print('')