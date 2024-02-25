import mysql.connector
import sqlite3
import colorama
from colorama import Fore

# Инициализация colorama для перехвата символов цвета в Windows
colorama.init(autoreset=True)

config = {
    'user': 'root',
    'password': 'qwe123',
    'host': '127.0.0.1',
    'database': 'sibplc',
    'raise_on_warnings': True,
}

sqlite3_company_dict = dict()
sqlite3_order_set = set()

maria_db_company_dict = dict()


def get_key_by_value(dictionary, val):
    #  функция, которая возвращает ключ словаря по значению.
    return next((k for k, v in dictionary.items() if v == val), None)


def create_maria_db_company_dict():  # создаём множество компаний из MariaDB
    # Устанавливаем соединение с БД MySQL
    connection_mysql = None
    cursor_mysql = None

    try:
        connection_mysql = mysql.connector.connect(**config)
        # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
        cursor_mysql = connection_mysql.cursor()
        # Выполняем SQL-запрос для получения названий всех таблиц
        # cursor.execute("SHOW TABLES")
        # Получаем результаты и выводим их
        # print("Названия всех таблиц в базе данных:")
        # tables = cursor.fetchall()
        # for (table_name,) in tables:
        #     print(table_name)

        cursor_mysql.execute("Select id, name FROM client")
        clients = cursor_mysql.fetchall()
        for client in clients:
            maria_db_company_dict[client[0]] = client[1]

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")

    finally:
        # Проверяем, был ли курсор инициализирован
        if cursor_mysql is not None:
            cursor_mysql.close()

        # Проверяем, было ли соединение установлено и открыто
        if connection_mysql is not None and connection_mysql.is_connected():
            connection_mysql.close()
            print("Соединение с базой данных MariaDB закрыто")


def create_sqlite3_order_set():  # создаём множество заказов из sqlite3
    with sqlite3.connect(r"../db.sqlite3") as connect:
        sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        sqlite3_cursor.execute("SELECT serial FROM main_order")
        all_row = sqlite3_cursor.fetchall()
    for row in all_row:
        sqlite3_order_set.add(row[0])
    print("sqlite3_order_set", sqlite3_order_set)
    print(len(sqlite3_order_set), "заказов в БД sqlite3")

    #     sqlite3_order_list = list()
    #     for row in all_row:
    #         # print(row[0])
    #         sqlite3_order_list.append(row[0])
    #     print(len(sqlite3_order_list), "заказов в БД sqlite3")
    #     # print("sqlite3_order_list", sqlite3_order_list)


def create_sqlite3_company_dict():  # Копирование компаний из SQlite3
    with sqlite3.connect(r"../db.sqlite3") as connect:
        sqlite3_cursor = connect.cursor()  # создаём курсор  для взаимодействия с БД
        sqlite3_cursor.execute("SELECT id, name FROM main_company")
        all_row = sqlite3_cursor.fetchall()
        for row in all_row:
            sqlite3_company_dict[row[0]] = row[1]
        print("sqlite3_company_dict", sqlite3_company_dict)


def import_order_from_maria_db_to_sqlite3_many():
    # тут мы займёмся импортированием заказов
    print("ща займёмся импортированием заказов")
    """
    connection_mysql = mysql.connector.connect(**config)
    # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
    cursor_mysql = connection_mysql.cursor()
    try:
        # Получаем данные из MySQL
        cursor_mysql.execute("SELECT serial, prio, status, name, client  FROM task")
        task = cursor_mysql.fetchall()
        print(len(task), "заказов в БД MySQL")

        # Создаем списки для пакетного выполнения операций
        insert_list = []
        update_list = []

        # Обходим полученные данные и заполняем списки
        for serial, priority, status, name, client in task:
            print("MariaDB_client_id", client)
            priority = 10 if priority == 0 else priority  # тернарный оператор
            if serial not in sqlite3_order_set:
                sqlite3_order_set.add(serial)
                insert_list.append((serial, priority, status, name))
                print("Заказ", serial, "будет внесён в БД SQlite3", "с приоритетом", priority, "статусом", status)
            else:
                update_list.append((priority, status, name, serial))
                print("Будет обновлён заказ", serial, "с приоритетом", priority, "статусом", status)

        # Выполняем пакетные операции INSERT и UPDATE

        if insert_list:
            sqlite_cursor.executemany("INSERT INTO main_order (serial, priority, status, name) VALUES (?, ?, ?, ?)",
                                      insert_list)

        if update_list:
            sqlite_cursor.executemany("UPDATE main_order SET priority = ?, status = ? , name = ? WHERE serial = ?",
                                      update_list)

        Коммитим один раз после всех операций
        sqlite_con.commit()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
            
        finally:
        if connection_mysql.is_connected():
            cursor_mysql.close()
            connection_mysql.close()
            print("Соединение с базой данных MySQL закрыто")
        
        # Закрываем соединение с SQLite
        sqlite_con.close()
"""


def company_comparison():  # сравнение данных о компаниях между MariaDB and SQlite
    # Создаем подключение к SQLite
    sqlite_con = sqlite3.connect(r"../db.sqlite3")
    # sqlite_cursor = sqlite_con.cursor()
    connection_mysql = mysql.connector.connect(**config)
    # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
    cursor_mysql = connection_mysql.cursor()
    try:
        # Получаем данные из MySQL
        cursor_mysql.execute("SELECT id, name FROM client")
        maria_db_all_client = cursor_mysql.fetchall()

        # Обходим полученные данные и заполняем списки
        for client_id, name in maria_db_all_client:
            print("MariaDB client", client_id, name, end=" ")
            print(Fore.GREEN + "ok") if (name in sqlite3_company_dict.values()) else print(Fore.RED + "err")

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")

    finally:
        if connection_mysql.is_connected():
            cursor_mysql.close()
            connection_mysql.close()
            print("Соединение с базой данных MySQL закрыто")

    # Закрываем соединение с SQLite
    sqlite_con.close()


def import_order_from_maria_db_to_sqlite3_one():  # Копирование номеров заказов из MariaDB в SQlite3 по одному
    # Устанавливаем соединение с БД MySQL
    connection_mysql = None
    cursor_mysql = None
    create_sqlite3_order_set()
    create_sqlite3_company_dict()
    create_maria_db_company_dict()
    try:
        connection_mysql = mysql.connector.connect(**config)
        # Создаем объект cursor, который позволяет нам выполнять SQL-запросы
        cursor_mysql = connection_mysql.cursor()
        cursor_mysql.execute("Select serial, prio, status, name, client FROM task")
        task = cursor_mysql.fetchall()
        print(len(task), "заказов в БД MySQL")
        for t in task:
            connect_sqlite3 = sqlite3.connect(r"D:\YandexDisk\MyProg\Python\my_django\SibPLC_KIS\db.sqlite3")
            cursor_sqlite3 = connect_sqlite3.cursor()
            serial = t[0]
            priority = t[1]
            status = t[2]
            name = t[3]
            # print("sqlite3_company_dict", sqlite3_company_dict)
            # print("maria_db_company_dict[t[4]]", maria_db_company_dict[t[4]])
            customer_id = get_key_by_value(sqlite3_company_dict, maria_db_company_dict[t[4]])
            if priority == 0:
                priority = None
            if priority == 10:
                priority = None
            if t[0] not in sqlite3_order_set:
                # добавляем строки в таблицу main_equipment
                cursor_sqlite3.execute("INSERT INTO main_order (serial, priority, status, name, customer_id )"
                                       " VALUES (?, ?, ?, ?, ?)", (serial, priority, status, name, customer_id,))
                # last_id = cursor_sqlite3.lastrowid
                connect_sqlite3.commit()  # выполняем транзакцию
                print("заявка", serial, "внесена в БД SQlite3")

            if t[0] in sqlite3_order_set:
                cursor_sqlite3.execute("UPDATE main_order SET priority=?, status=?, name=?, customer_id=?"
                                       " WHERE serial = ?", (priority, status, name, customer_id, serial,))
                connect_sqlite3.commit()  # выполняем транзакцию
                print("для заявки", serial, "   обновлён приоритет", priority, "   статус", status, "   имя", name,
                      "   заказчик", sqlite3_company_dict[customer_id])


        # mysql_order_list = list()
        # for t in task:
        #     mysql_order_list.append(t[0])
        # print(len(mysql_order_list), "заказов в БД MySQL")
        #
        # for t in task:
        #     count = mysql_order_list.count(t[0])
        #     if count > 1:
        #         print(t[0], count)

    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")

    finally:
        # Проверяем, был ли курсор инициализирован
        if cursor_mysql is not None:
            cursor_mysql.close()

        # Проверяем, было ли соединение установлено и открыто
        if connection_mysql is not None and connection_mysql.is_connected():
            connection_mysql.close()
            print("Соединение с базой данных MariaDB закрыто")


answer = ""
# Copying the automation cabinets inventory table
while answer != "0":
    answer = input("Что будем делать? \n"
                   "0: exit \n"
                   "1: create sqlite3_company_dict \n"
                   "2: company_comparison\n"
                   "3: create_sqlite3_order_set\n"
                   "4: create_maria_db_company_dict\n"
                   "5: import_order_from_maria_db_to_sqlite3_one\n")
    if answer == "0":
        print("прощайте")
    elif answer == "1":
        print("create_sqlite3_company_dict()")
        create_sqlite3_company_dict()
    elif answer == "2":
        create_sqlite3_company_dict()
        print("Сравниваем данные о клиентах")
        print(Fore.GREEN + "ok", end=' ')
        print("клиент из MariaDB есть в SQlite")
        print(Fore.RED + "err", end=' ')
        print("клиента из MariaDB НЕТУ в SQlite")
        company_comparison()
    elif answer == "3":
        print("create_sqlite3_order_set()")
        create_sqlite3_order_set()
    elif answer == "4":
        print("create_maria_db_company_dict()")
        create_maria_db_company_dict()
        print("maria_db_company_dict", maria_db_company_dict)
    elif answer == "5":
        print("import_order_from_maria_db_to_sqlite3_one")
        import_order_from_maria_db_to_sqlite3_one()
    else:
        print("неверный ввод ")
    print(" ")
