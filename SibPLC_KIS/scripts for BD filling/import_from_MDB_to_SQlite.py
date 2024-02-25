import pyodbc
import sqlite3
import colorama
# from datetime import date
from datetime import datetime
from colorama import Fore

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)

sqlite3_db_path = r"D:\YandexDisk\MyProg\Python\Django\SibPLC_KIS_v2\SibPLC_KIS\db.sqlite3"
sqlite3_person_dict = {}  # словарь людей
sqlite3_box_accounting_list = []  # список записей серийников шкафов
sqlite3_company_dict = dict()  # словарь всех компаний ключ-id, значение-имя
sqlite3_order_list = []  # список номеров всех заказов строка формата nnn-mm-yyyy

# Строка подключения, которая дословно передается менеджеру драйверов.
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\YandexDisk\db\Data_Base_Sibplc_v13.mdb"
)

MDB_dict_persons = dict()  # словарь людей


def get_key_by_value(dictionary, val):
    #  функция, которая возвращает ключ словаря по значению.
    return next((k for k, v in dictionary.items() if v == val), None)


def create_mdb_dict_persons():
    with pyodbc.connect(conn_str) as cnxn:
        # Прежде всего, получим все данные
        with cnxn.cursor() as select_cursor:
            select_cursor.execute("SELECT * FROM Persons ORDER BY Surname")
            data = select_cursor.fetchall()
            for row in data:
                MDB_dict_persons[row.ID] = row.Surname + row.Name_1
            print("MDB_dict_persons", MDB_dict_persons)
            print("")


def create_sqlite3_person_dict():
    # функция создаёт словарь людей из БД sqlite3
    # ключ id
    # значение ФамилияИмя
    # this function is not pure
    with sqlite3.connect(sqlite3_db_path) as connect:
        sqlite3_cursor = connect.cursor()
        sqlite3_cursor.execute("SELECT id, surname, name FROM main_person")
        all_row = sqlite3_cursor.fetchall()
        # print("all_row ", all_row)
        for row in all_row:
            sqlite3_person_dict[row[0]] = row[1] + row[2]
        print("sqlite3_person_dict ", sqlite3_person_dict)
        # print("row ", row)


def create_sqlite3_box_accounting_list():
    # сперва выгрузим существующие записи из sqlite3
    with sqlite3.connect(sqlite3_db_path) as connect:
        sqlite3_cursor = connect.cursor()
        sqlite3_cursor.execute("SELECT serial_num FROM main_box_accounting")
        all_row = sqlite3_cursor.fetchall()
        for row in all_row:
            sqlite3_box_accounting_list.append(row[0])
        sqlite3_box_accounting_list.sort()
        print("список записей о серийных номерах шкафов из БД sqlite3:")
        print("sqlite3_box_accounting_list", sqlite3_box_accounting_list)
        print()


def create_sqlite3_order_list():
    with sqlite3.connect(sqlite3_db_path) as connect:
        sqlite3_cursor = connect.cursor()
        sqlite3_cursor.execute("SELECT serial FROM main_order")
        all_row = sqlite3_cursor.fetchall()
        for row in all_row:
            sqlite3_order_list.append(row[0])
        print("sqlite3_order_list", sqlite3_order_list)


def create_sqlite3_company_dict():
    with sqlite3.connect(sqlite3_db_path) as connect:
        sqlite3_cursor = connect.cursor()
        sqlite3_cursor.execute("SELECT id, name FROM main_company")
        all_row = sqlite3_cursor.fetchall()
        for row in all_row:
            sqlite3_company_dict[row[0]] = row[1]
        print("sqlite3_company_dict", sqlite3_company_dict)


def copy_box_from_mdb_to_sqlite():  # Копирование таблицы учёта шкафов из БД MDB в БД SQlite3
    print("Копирование таблицы учёта шкафов из БД MDB в БД SQlite3")
    create_sqlite3_company_dict()
    create_sqlite3_order_list()
    create_sqlite3_box_accounting_list()
    create_sqlite3_person_dict()
    create_mdb_dict_persons()

    # Чтение данных о шкафах из MDB и перенос в sqlite3
    print("Чтение данных о шкафах из MDB")
    with pyodbc.connect(conn_str) as cnxn:
        # Прежде всего, получим все данные
        with cnxn.cursor() as select_cursor:
            select_cursor.execute("SELECT * FROM Uchet_SHA ORDER BY serial_num ASC")
            data = select_cursor.fetchall()

            # mdb_serial_num_list = []
            # num = 73
            for row in data:
                # print(row.serial_num)
                print("жопа") if not row.tester_id else None
                # mdb_serial_num_list.append(row.serial_num)

                # if row.order_num in sqlite3_order_list:
                #     sqlite3_order_id = row.order_num
                #     print(Fore.GREEN + "серийный номер шкафа " + str(row.serial_num) +
                #           "   заявка " + row.order_num + "   заказчик " + row.customer)
                # else:
                #     print(Fore.RED + "заказ " + row.order_num + " не найден " + str(row.serial_num))

                if row.order_num not in sqlite3_order_list:
                    print(Fore.RED + "заказ " + row.order_num + " не найден " + str(row.serial_num))
                elif MDB_dict_persons[row.assembler_id] not in sqlite3_person_dict.values():
                    print(Fore.RED + "сборщик " + MDB_dict_persons[row.assembler_id] +
                          " не найден в БД SQlite3, с/н шкафа  " + str(row.serial_num))
                elif MDB_dict_persons[row.scheme_developer_id] not in sqlite3_person_dict.values():
                    print(Fore.RED + "разработчик схемы " + MDB_dict_persons[row.scheme_developer_id] +
                          " не найден в БД SQlite3, с/н шкафа  " + str(row.serial_num))
                elif row.programmer_id and MDB_dict_persons[row.programmer_id] not in sqlite3_person_dict.values():
                    print(Fore.RED + "разработчик ПО " + MDB_dict_persons[row.programmer_id] +
                          " не найден в БД SQlite3, с/н шкафа  " + str(row.serial_num))
                elif row.tester_id and MDB_dict_persons[row.tester_id] not in sqlite3_person_dict.values():
                    print(Fore.RED + "Тестировщик " + MDB_dict_persons[row.tester_id] +
                          " не найден в БД SQlite3, с/н шкафа  " + str(row.serial_num))
                else:
                    # внесение в базу серийников которых нет
                    # print(Fore.GREEN + "все участники найдены")
                    if row.serial_num not in sqlite3_box_accounting_list:
                        sqlite3_order_id = row.order_num
                        sqlite3_person_id = get_key_by_value(sqlite3_person_dict, MDB_dict_persons[row.assembler_id])
                        sqlite3_scheme_developer_id = get_key_by_value(sqlite3_person_dict,
                                                                       MDB_dict_persons[row.scheme_developer_id])
                        if row.programmer_id:
                            sqlite3_programmer_id = get_key_by_value(sqlite3_person_dict,
                                                                     MDB_dict_persons[row.programmer_id])
                        else:
                            sqlite3_programmer_id = None
                        sqlite3_tester_id = get_key_by_value(sqlite3_person_dict,
                                                             MDB_dict_persons[row.tester_id])
                        with sqlite3.connect(sqlite3_db_path) as connect:
                            sqlite3_cursor = connect.cursor()
                            sqlite3_cursor.execute("INSERT INTO main_box_accounting "
                                                   "(serial_num, name, order_id, "
                                                   "assembler_id, "
                                                   "scheme_developer_id, "
                                                   "programmer_id, "
                                                   "tester_id)"
                                                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                                   (int(row.serial_num),
                                                    row.box_name,
                                                    sqlite3_order_id,
                                                    sqlite3_person_id,
                                                    sqlite3_scheme_developer_id,
                                                    sqlite3_programmer_id,
                                                    sqlite3_tester_id)
                                                   )
                            connect.commit()  # выполняем транзакцию
                            print(Fore.GREEN + "добавлена запись с серийным номером " + str(row.serial_num))
                            print("")
    #
    #             # отдельно вносится ФИО сборщика
    #             if row.assembler_id:
    #                 print("MDB assembler_id", row.assembler_id, end=" ")
    #                 print(MDB_dict_persons[row.assembler_id])
    #                 if MDB_dict_persons[row.assembler_id] in sqlite3_person_dict.values():
    #                     sqlite3_person_id = get_key_by_value(sqlite3_person_dict, MDB_dict_persons[row.assembler_id])
    #                     print("sqlite3_person_id", sqlite3_person_id, end=" ")
    #                     print(sqlite3_person_dict[sqlite3_person_id])
    #                     with sqlite3.connect(
    #                             r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
    #                         sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
    #                         sqlite3_cursor.execute(
    #                             "UPDATE main_box_accounting "
    #                             "SET assembler_id = ? "
    #                             "WHERE serial_num = ?",
    #                             (sqlite3_person_id, row.serial_num))
    #                         con.commit()  # выполняем транзакцию
    #
    #             print("")


# ------------------------------------------Копирование таблицы городов-----------------------------------------------
def copy_city_from_mdb_to_sqlite():  # Копирование таблицы учёта шкафов из БД MDB в БД SQlite3
    with sqlite3.connect(sqlite3_db_path) as connect:
        sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        sqlite3_cursor.execute("SELECT name FROM main_city")

        all_row = sqlite3_cursor.fetchall()

        sqlite3_city_set = set()
        for row in all_row:
            # print(row[0])
            sqlite3_city_set.add(row[0])

        # print("sqlite3_city_list", sqlite3_city_list)

    # Подключаемся к исходной базе данных MDB и выбираем данные
    with pyodbc.connect(conn_str) as cnxn:
        select_cursor = cnxn.cursor()
        select_cursor.execute("SELECT * FROM City")
        data = select_cursor.fetchall()

    # Подключаемся к SQLite базе данных для выполнения всех вставок
    with sqlite3.connect(sqlite3_db_path) as con:
        cursor = con.cursor()

        # Подготавливаем запрос заранее
        insert_query = "INSERT INTO main_city (name) VALUES (?)"

        # Проходим по данным для вставки новых городов
        for row in data:
            if row.Name not in sqlite3_city_set:
                print(Fore.GREEN + "надо внести " + row.Name)
                cursor.execute(insert_query, (row.Name,))

        # Фиксируем изменения одной транзакцией
        con.commit()


# Получаем текущую дату и время
now = datetime.now()

# Получаем только дату без времени
current_date = now.date()

# Печатаем драйвер
# print(pyodbc.drivers())

answer = ""
# Copying the automation cabinets inventory table
while answer != "0":
    answer = input("Что будем делать? \n"
                   "0: exit \n"
                   "1: create_sqlite3_person_dict \n"
                   "2: create_sqlite3_box_accounting_list \n"
                   "3: create_sqlite3_order_list \n"
                   "4: create_sqlite3_company_dict \n"
                   "5: copy_box_from_mdb_to_sqlite \n"
                   "6: copy_city_from_mdb_to_sqlite \n")
    if answer == "1":
        print("creating sqlite3 dictionary person")
        create_sqlite3_person_dict()
    if answer == "2":
        print("creating sqlite3 box accounting list")
        create_sqlite3_box_accounting_list()
    if answer == "3":
        print("creating sqlite3 order list")
        create_sqlite3_order_list()
    if answer == "4":
        print("create_sqlite3_company_dict")
        create_sqlite3_company_dict()
    if answer == "5":
        print("copy_box_from_mdb_to_sqlite()")
        copy_box_from_mdb_to_sqlite()
    if answer == "6":
        print("copy_city_from_mdb_to_sqlite()")
        copy_city_from_mdb_to_sqlite()
    print("")

# # Читаем таблицу шкафов из MDB

# with pyodbc.connect(conn_str) as cnxn:
#     # Прежде всего, получим все данные
#     with cnxn.cursor() as select_cursor:
#         select_cursor.execute("SELECT * FROM Box")
#         data = select_cursor.fetchall()
#
#     # Теперь прочитаем данные
#     with cnxn.cursor() as update_cursor:
#         for row in data:
#             # print(row)
#             # print("Свойства:")
#             #
#             # print("ID:", row.ID)
#             # print("Manufacturer:", row.Manufacturer)
#             # print("Model:", row.Model)
#             # print("Name:", row.Name)
#             # print("Vendor code:", row.Vendor_code)
#             # print("Note:", row.Note)
#             # print("Material:", row.Material)
#             # print("H:", row.H)
#             # print("W:", row.W)
#             # print("D:", row.D)
#             # print("IP:", row.IP)
#             # print("")
#             pass
# cnxn.close()
#
# # подключаемся к БД sqlite3
# dict_model = dict()
# with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
#     sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
#
#     # формируем словарь производителей
#     sqlite3_cursor.execute("SELECT id, name FROM main_manufacturers")
#     all_row = sqlite3_cursor.fetchall()
#     # print(all_row)
#
#     dict_manufacturers_sqlite = dict()
#     for row in all_row:
#         dict_manufacturers_sqlite[row[0]] = row[1]
#         # print(row)
#     # print(dict_manufacturers_sqlite)
#
#     # формируем словарь степеней защиты корпусов
#     print()
#     sqlite3_cursor.execute("SELECT id, name FROM main_boxip")
#     all_row = sqlite3_cursor.fetchall()
#     # print(all_row)
#     dict_box_ip_sqlite = dict()
#     for row in all_row:
#         dict_box_ip_sqlite[row[0]] = row[1]
#         # print(row)
#     # print(dict_box_ip_sqlite)
#     # print()
#
#     # формируем словарь материалов корпусов
#     sqlite3_cursor.execute("SELECT id, name FROM main_boxmaterial")
#     all_row = sqlite3_cursor.fetchall()
#     # print(all_row)
#     dict_box_material_sqlite = dict()
#     for row in all_row:
#         dict_box_material_sqlite[row[0]] = row[1]
#         # print(row)
#     # print(dict_box_material_sqlite)
#     print()
#
#     sqlite3_cursor.execute("SELECT vendore_code FROM main_equipment")
#     i = 0
#     # while True:
#     #     one_row = cursor.fetchone()
#     #     if not one_row:
#     #         break
#     #     if one_row:
#     #         dict_model[i] = one_row[0]
#     #         i += 1
#     # print(dict_model)
#
#     all_row = sqlite3_cursor.fetchall()
#     # print(type(all_row))
#     # print(type(all_row[0]))
#     # print(all_row)
#
#     # формируем список Артикулов
#     sqlite3_vendore_code_list = list()
#     for row in all_row:
#         # print(row[0])
#         sqlite3_vendore_code_list.append(row[0])
#
#     # print("sqlite3_vendore_code_list", sqlite3_vendore_code_list)
#
#
# def adapt_date(val):
#     return val.isoformat()
#
#
# def convert_date(val):
#     return datetime.strptime(val.decode(), "%Y-%m-%d")
#
#
# # Then tell sqlite3 to use these functions for the conversion
# sqlite3.register_adapter(date, adapt_date)
# sqlite3.register_converter("date", convert_date)
#
# # ------------------------------------------Копирование таблицы корпусов шкафов------------------------------------
# with pyodbc.connect(conn_str) as cnxn:
#     # Прежде всего, получим все данные
#     with cnxn.cursor() as select_cursor:
#         select_cursor.execute("SELECT * FROM Box")
#         data = select_cursor.fetchall()
#
#     # Теперь прочитаем данные
#     with cnxn.cursor() as cursor:
#         for row in data:
#             # print(row)
#             if row.Vendor_code not in sqlite3_vendore_code_list:
#                 print("надо внести", row.Vendor_code)
#
#                 con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
#                 sqlite3_cursor = con.cursor()
#                 # добавляем строки в таблицу main_equipment
#                 name = row.Name
#                 price = int(row.Price_RUR)
#                 relevance = True  # актуальность
#                 price_date = current_date
#                 description = row.Note
#                 vendore_code = row.Vendor_code
#                 model = row.Model
#                 currency_id = 1
#                 type_id = 16
#
#                 manufacturer = row.Manufacturer
#                 for key, value in dict_manufacturers_sqlite.items():
#                     if value == manufacturer:
#                         manufacturer_id = key
#                 # manufacturer_id = get_key(dict_manufacturers_sqlite, row.Manufacturer)
#
#                 for key, value in dict_box_ip_sqlite.items():
#                     if str(row.IP) in value:
#                         ip_id = key
#
#                 material = row.Material
#                 for key, value in dict_box_material_sqlite.items():
#                     if value == material:
#                         id_material = key
#
#                 sqlite3_cursor.execute(
#                     "INSERT INTO main_equipment (name, price, relevance, price_date, description, vendore_code, "
#                     "model, currency_id, type_id, manufacturer_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                     (name, price, relevance, price_date, description, vendore_code, model, currency_id, type_id,
#                      manufacturer_id)
#                 )
#                 last_id = sqlite3_cursor.lastrowid
#                 con.commit()  # выполняем транзакцию
#
#                 sqlite3_cursor.execute(
#                     "INSERT INTO main_box (height, width, depth, material_id, equipment_id, ip_id)"
#                     " VALUES ( ?, ?, ?, ?, ?, ?)",
#                     (row.H, row.W, row.D, id_material, last_id, ip_id)
#                 )
#                 con.commit()  # выполняем транзакцию
# cnxn.close()
#

#
# # ----------------------------------------Копирование таблицы людей--------------------------------------------------
# with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
#     sqlite3_cursor = connect.cursor()
#     sqlite3_cursor.execute("SELECT id,name FROM main_company")
#     all_row = sqlite3_cursor.fetchall()
#     sqlite3_company_dict = {}  # словарь компаний
#     for row in all_row:
#         sqlite3_company_dict.update({row[0]: row[1]})
#     # print("sqlite3_company_dict ", sqlite3_company_dict)
#
# with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
#     sqlite3_cursor = connect.cursor()
#     sqlite3_cursor.execute("SELECT * FROM main_person")
#
#     # Получение названий столбцов из description с помощью обычного for-цикла
#     column_names = []
#     for description in sqlite3_cursor.description:
#         column_names.append(description[0])
#
#     # print("column names of the table main_person:", column_names)
#
# with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
#     sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
#     sqlite3_cursor.execute("SELECT surname, name, patronymic   FROM main_person")
#
#     all_row = sqlite3_cursor.fetchall()
#
#     sqlite3_person_list = list()
#     for row in all_row:
#         # print(f"{row[0]} {row[1]} {row[2]}" )
#         sqlite3_person_list.append(f"{row[0]} {row[1]} {row[2]}")
#
#     # print("sqlite3_person_list", sqlite3_person_list)
#
# with pyodbc.connect(conn_str) as cnxn:
#     # Прежде всего, получим все данные
#     with cnxn.cursor() as select_cursor:
#         select_cursor.execute("SELECT * FROM Persons ORDER BY Surname")
#         data = select_cursor.fetchall()
#
#         MDB_dict_persons = dict()
#         for row in data:
#             MDB_dict_persons[row.ID] = row.Surname + row.Name_1
#         print("MDB_dict_persons", MDB_dict_persons)
#         print("")
#
#     # Теперь прочитаем данные
#     with cnxn.cursor() as cursor:
#         for row in data:
#             # print(row)
#
#             if f"{row.Surname} {row.Name_1} {row.Name_2}" not in sqlite3_person_list:
#                 print("надо внести", f"{row.Surname} {row.Name_1} {row.Name_2}")
#
#                 con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
#                 cursor = con.cursor()
#                 # добавляем строки в таблицу main_equipment
#                 name = row.Name_1
#
#                 patronymic = row.Name_2
#                 surname = row.Surname
#                 phone = row.Phone
#                 email = row.Email
#
#                 company = row.Company
#                 for key, value in sqlite3_company_dict.items():
#                     if value == company:
#                         company_id = key
#
#                 cursor.execute(
#                     "INSERT INTO main_person (name, patronymic, surname, phone, email, company_id)"
#                     " VALUES (?, ?, ?, ?, ?, ?)",
#                     (name, patronymic, surname, phone, email, company))
#                 last_id = cursor.lastrowid
#                 con.commit()  # выполняем транзакцию
# cnxn.close()
#
# # --------------------------------------Копирование таблицы компаний-------------------------------------------------
# with sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3") as connect:
#     sqlite3_cursor = connect.cursor()
#
#     # формируем словарь форм компаний из БД sqlite3. Ключ это id записи. Значение это название формы компании
#     sqlite3_cursor.execute("SELECT id,name FROM main_companiesform")
#     all_row = sqlite3_cursor.fetchall()
#     sqlite3_companies_form_dict = {}  # словарь форм компаний
#     for row in all_row:
#         sqlite3_companies_form_dict.update({row[0]: row[1]})
#     # print("sqlite3_companiesform_dict ",sqlite3_companiesform_dict)
#
#     # формируем словарь городов. Ключ это id записи. Значение это название города
#     sqlite3_cursor.execute("SELECT id,name FROM main_city")
#     all_row = sqlite3_cursor.fetchall()
#     sqlite3_city_dict = {}  # словарь форм городов
#     for row in all_row:
#         sqlite3_city_dict.update({row[0]: row[1]})
#     # print("sqlite3_city_dict ", sqlite3_city_dict)
#
#     # Получение названий столбцов из description с помощью обычного for-цикла
#     sqlite3_cursor.execute("SELECT * FROM main_company")
#     column_names = []
#     for description in sqlite3_cursor.description:
#         column_names.append(description[0])
#     # print("column names of the table main_company :", column_names)
#
#     # Формирование списка и словаря компаний из БД sqlite3
#     sqlite3_cursor.execute("SELECT name FROM main_company")
#     all_row = sqlite3_cursor.fetchall()
#     sqlite3_company_list = list()
#     sqlite3_company_dict = dict()
#     for row in all_row:
#         # print(f"{row[0]}")
#         sqlite3_company_list.append(f"{row[0]}")
#     # print("sqlite3_company_list", sqlite3_company_list)
#
# # создаём словарь городов из MDB
# with pyodbc.connect(conn_str) as cnxn:
#     with cnxn.cursor() as select_cursor:
#         select_cursor.execute("SELECT * FROM City")
#         data = select_cursor.fetchall()
#         mdb_city_dict = {}
#         for row in data:
#             mdb_city_dict.update({row[0]: row[1]})
#             # print(row)
#         # print("mdb_city_dict ", mdb_city_dict)
#
# # Чтение данных о компанийх из MDB и перенос в sqlite3
# with pyodbc.connect(conn_str) as cnxn:
#     # Прежде всего, получим все данные
#     with cnxn.cursor() as select_cursor:
#         select_cursor.execute("SELECT * FROM Companies")
#         data = select_cursor.fetchall()
#         # for row in data:
#         # print(row)
#
#     # Теперь прочитаем данные
#     with cnxn.cursor() as cursor:
#         for row in data:
#             # print(row)
#
#             if f"{row.Company}" not in sqlite3_company_list:
#                 print("надо внести", f"{row.Company}")
#                 name = row.Company
#                 company_form = row.Form
#                 # print(company_form)
#                 company_form_id = company_form
#
#                 mdb_city_id = row.City
#                 city_name = mdb_city_dict[mdb_city_id]
#                 # print(city_name)
#                 for key, value in sqlite3_city_dict.items():
#                     if city_name == value:
#                         sqlite3_city_id = key
#                         # print("sqlite3_city_id", sqlite3_city_id)
#
#                 con = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
#                 cursor = con.cursor()
#                 cursor.execute("INSERT INTO main_company (name, city_id, form_id) VALUES (?, ?, ?)",
#                                (name, sqlite3_city_id, company_form_id))
#                 last_id = cursor.lastrowid
#                 con.commit()  # выполняем транзакцию
# cnxn.close()
#


# анализ целостности серийников
# mdb_serial_num_list.sort()
# print(mdb_serial_num_list)
# print(len(mdb_serial_num_list))
# for i in range(1, len(mdb_serial_num_list) - 1):
#     # print(row.serial_num)
#     if (mdb_serial_num_list[i] - 1) != (mdb_serial_num_list[i-1]):
#         print('жопа', mdb_serial_num_list[i])
# # анализ показал что не хватает 29+9 записей, т.е мы собрали на 38 шкафов меньше чем текущий серийный номер
