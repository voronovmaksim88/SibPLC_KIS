import xlrd
import sqlite3
from datetime import datetime

# Получаем текущую дату и время
now = datetime.now()

# Получаем только дату без времени
current_date = now.date()

# Выводим дату в консоль
print(current_date)

"""-------------------------------- Импорт стран из таблицы exel в БД джанго---------------------------------------"""
answer = input("copy countries from the exel table? y/n ")
if answer == "y":
    answer = ""
    book = xlrd.open_workbook(r"D:\YandexDisk\db\Countries.xls")
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    print("{0} rows={1} columns={2}".format(sh.name, sh.nrows, sh.ncols))

    for rx in range(sh.nrows):
        print(sh.row(rx))

    print("id is {0}".format(int(sh.cell_value(rowx=1, colx=0))), end=", ")  # id
    print("country is {0}".format(sh.cell_value(rowx=1, colx=1)))  # country

    con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
    cursor = con.cursor()

    # добавляем строки в таблицу Countries
    cursor.execute("DELETE FROM app_countries;")  # полностью чистим данные таблицы
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'app_countries';")  # скидываем счётчик id в ноль
    con.commit()  # выполняем транзакцию

    for rx in range(1, sh.nrows):
        cursor.execute(
            "INSERT INTO app_countries (name) VALUES ('{0}')".format(sh.cell_value(rowx=rx, colx=1)))  # country
        con.commit()  # выполняем транзакцию

"""------------------------------ Импорт производителей из таблицы exel в БД джанго -------------------------------"""
answer = input("copy manufacturers from the exel table? y/n ")
if answer == "y":
    answer = ""
    book = xlrd.open_workbook(r"D:\YandexDisk\db\Manufacturers.xls")
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    print("{0} rows={1} columns={2}".format(sh.name, sh.nrows, sh.ncols))
    for rx in range(sh.nrows):
        print(sh.row(rx))

    con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
    cursor = con.cursor()

    # добавляем строки в таблицу manufacturers
    cursor.execute("DELETE FROM app_manufacturers;")  # полностью чистим данные таблицы
    cursor.execute(
        "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'app_manufacturers';")  # скидываем счётчик id в ноль
    con.commit()  # выполняем транзакцию

    for rx in range(1, sh.nrows):
        name = sh.cell_value(rowx=rx, colx=1)
        country_id = sh.cell_value(rowx=rx, colx=2)
        cursor.execute(
            "INSERT INTO app_manufacturers (name, country_id) VALUES (?, ?)", (name, country_id)
        )
    con.commit()  # выполняем транзакцию

"""---------------------- Импорт типов оборудования из БД электронных компонентов в БД джанго ----------------------"""
answer = input("copy Electronic_Components from the exel db.sqlite3? y/n ")
if answer == "y":
    answer = ""

    con1 = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
    cur1 = con1.cursor()

    con2 = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\SibPLC_Electronic_Components_DB\electronic_equipment.db")
    cur2 = con2.cursor()

    cur1.execute("DELETE FROM main_equipmenttype;")  # полностью чистим данные таблицы
    cur1.execute(
        "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_equipmenttype';")  # скидываем счётчик id в ноль
    con1.commit()  # выполняем транзакцию

    cur2.execute("SELECT name FROM type_of_components ")
    one_row = cur2.fetchone()
    while one_row:
        print(one_row)
        cur1.execute(
            "INSERT INTO main_equipmenttype (name) VALUES ('{0}')".format(one_row[0]))
        one_row = cur2.fetchone()
        con1.commit()  # выполняем транзакцию

"""----------------------   Импорт таблицы корпусов для шкафов из таблицы exel в БД джанго  ----------------------"""
answer = input("copy Box from the exel table? y/n ")
if answer == "y":
    answer = ""
    # создаём словарь производителей
    dict_manufacturer = {}
    with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
        cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        cursor.execute("SELECT id, name FROM main_manufacturers")
        while True:
            one_row = cursor.fetchone()
            if not one_row:
                break
            if one_row:
                dict_manufacturer[one_row[0]] = one_row[1]
    print(dict_manufacturer)

    book = xlrd.open_workbook(r"D:\YandexDisk\db\Box.xls")
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    print("{0} rows={1} columns={2}".format(sh.name, sh.nrows, sh.ncols))
    for rx in range(sh.nrows):
        print(sh.row(rx))

    con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
    cursor = con.cursor()

    # добавляем строки в таблицу main_equipment
    cursor.execute("DELETE FROM main_equipment;")  # полностью чистим данные таблицы
    cursor.execute(
        "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'main_equipment';")  # скидываем счётчик id в ноль
    con.commit()  # выполняем транзакцию

    for rx in range(1, sh.nrows):
        name = sh.cell_value(rowx=rx, colx=3)
        price = sh.cell_value(rowx=rx, colx=11)
        relevance = True
        price_date = current_date
        description = sh.cell_value(rowx=rx, colx=5)
        vendore_code = sh.cell_value(rowx=rx, colx=4)
        model = sh.cell_value(rowx=rx, colx=2)
        currency_id = 1
        type_id = 16

        manufacturer_id = ""
        manufacturer = sh.cell_value(rowx=rx, colx=1)
        for key, value in dict_manufacturer.items():
            if value == manufacturer:
                manufacturer_id = key

        cursor.execute(
            "INSERT INTO main_equipment (name, price, relevance, price_date, description, vendore_code, model,"
            " currency_id, type_id, manufacturer_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                name, price, relevance, price_date, description, vendore_code, model, currency_id, type_id,
                manufacturer_id)
        )
    con.commit()  # выполняем транзакцию
