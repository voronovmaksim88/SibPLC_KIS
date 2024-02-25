# pip install colorama
import xlrd
import sqlite3
from datetime import datetime
import colorama
from colorama import Fore

# Получаем текущую дату и время
now = datetime.now()

# Получаем только дату без времени
current_date = now.date()

# Выводим дату в консоль
print(current_date)

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)


def print_person(order_col_id):
    print(Fore.BLUE + str(sh.cell(0, order_col_id).value))
    for row_x in range(1, sh.nrows):  # начинаем с 1, чтобы пропустить заголовок
        cell_x = sh.cell(row_x, order_col_id)
        if cell_x.value != "":
            print(cell_x.value, end=" ")
            if cell_x.value in person_list:
                print(Fore.GREEN + "+")
            else:
                print(Fore.RED + "нет в базе !!!")
    print("")


"""--------------------------   Импорт серийных номеров шкафов из таблицы exel в БД джанго  ------------------------"""
answer = input("copy serial numbers of Box from the exel table to sqlite3? y/n ")
if answer == "y":
    answer = ""

    # создаём словарь компаний
    dict_company = {}
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT id, name FROM main_company")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                dict_company[one_row[0]] = one_row[1]
    print(dict_company)

    # создаём список заказов
    order_list = []
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT serial FROM main_order")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                order_list.append(one_row[0])
    print("order_list", order_list, end=" ")
    print("")

    # создаём список людей
    person_list = []
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT surname FROM main_person")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                person_list.append(one_row[0])
    print("person_list", person_list, end=" ")
    print("")

    # создаём словарь людей, так как нам потом нужны будут их id
    dict_person = {}
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT id, surname FROM main_person")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                dict_person[one_row[0]] = one_row[1]
    print('dict_person', dict_person)

    # создаём список серийных номеров шкафов
    box_serial_num_list = []
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT serial_num FROM main_box_accounting")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                box_serial_num_list.append(one_row[0])
    print("box_serial_num_list", box_serial_num_list)
    print("")

    book = xlrd.open_workbook(r"D:\YandexDisk\Труд\0_В работе\Учёт шкафов до 2019_р1.xls")
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    print("{0} rows={1} columns={2}".format(sh.name, sh.nrows, sh.ncols))
    for rx in range(sh.nrows):
        print(sh.row(rx))
    print("")

    # Выводим данные из колонки "Заказчик"
    order_col_idx = 3
    print(Fore.BLUE + str(sh.cell(0, order_col_idx).value))
    for rx in range(1, sh.nrows):  # начинаем с 1, чтобы пропустить заголовок
        order_cell = sh.cell(rx, order_col_idx)
        print(order_cell.value, end=" ")
        if order_cell.value in dict_company.values():
            print(Fore.GREEN + "+")
        else:
            print(Fore.RED + " нет в базе !!! ")

    order_col_idx = 2
    # начинаем выводить данные из колонки "номер заказа"
    for rx in range(1, sh.nrows):  # начинаем с 1, чтобы пропустить заголовок
        serial_cell = sh.cell(rx, order_col_idx)
        print(serial_cell.value, end=" ")
        if serial_cell.value in order_list:
            print(Fore.GREEN + "+")
        else:
            print(Fore.RED + " нет в базе !!! ")
    print("")

    # Выводим данные из колонки "разработчик схемы"
    print_person(4)

    # Выводим данные из колонки "разработчик схемы (scheme_developer)"
    print_person(5)

    # Выводим данные из колонки "assembler (сборщик)"
    print_person(6)

    # Выводим данные из колонки "тестировщик (tester)"
    print_person(7)

    # добавляем строки в таблицу box_accounting
    for rx in range(1, sh.nrows):
        serial_num = sh.cell_value(rowx=rx, colx=0)
        name = sh.cell_value(rowx=rx, colx=1)
        order = sh.cell_value(rowx=rx, colx=2)
        client = sh.cell_value(rowx=rx, colx=3)
        scheme_developer = sh.cell_value(rowx=rx, colx=4)
        programmer = sh.cell_value(rowx=rx, colx=5)
        assembler = sh.cell_value(rowx=rx, colx=6)
        tester = sh.cell_value(rowx=rx, colx=7)

        client_id = ""
        for key, value in dict_company.items():
            if value == client:
                client_id = key

        scheme_developer_id = ""
        for key, value in dict_person.items():
            if value == scheme_developer:
                scheme_developer_id = key

        programmer_id = ""
        if programmer not in dict_person.values():
            programmer_id = None
        else:
            for key, value in dict_person.items():
                if value == programmer:
                    programmer_id = key

        assembler_id = ""
        for key, value in dict_person.items():
            if value == assembler:
                assembler_id = key

        tester_id = ""
        for key, value in dict_person.items():
            if value == tester:
                tester_id = key

        if serial_num not in box_serial_num_list:
            with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
                cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД

                cursor.execute(
                    "INSERT INTO main_box_accounting "
                    "(serial_num, name, order_id, scheme_developer_id, assembler_id, programmer_id, tester_id)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (int(serial_num), name, order, scheme_developer_id, assembler_id, programmer_id, tester_id)
                )
                print("внесён серийный номер", serial_num, )

        if order in order_list:
            with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
                cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД

                cursor.execute(
                    "UPDATE main_order SET customer_id = ? WHERE serial = ? ",
                    (client_id, order)
                )
                print("изменена запись для заказа", order)

