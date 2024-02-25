import mysql.connector
from colorama import Fore, init, Style
from contextlib import contextmanager

init(autoreset=True)

# Ваши данные для подключения
config = {
    'user': 'max_work',
    'password': 'qwe123',
    'host': 'ovz1.9138995941.me2jm.vps.myjino.ru',
    'database': 'sibplc',
    'port': 49160  # Указываем порт подключения к базе данных
}


@contextmanager
def mysql_connection(conn_config):
    """Контекстный менеджер для соединения с MySQL"""
    connet = mysql.connector.connect(**conn_config)
    try:
        yield connet
    finally:
        connet.close()


# Использование созданного контекстного менеджера для управления соединением
with mysql_connection(config) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Список таблиц:")
        for (table_name,) in tables:
            print(Fore.LIGHTGREEN_EX + table_name)

# После выхода из блока with соединение будет автоматически закрыто.
"""
import logging
from sshtunnel import SSHTunnelForwarder
import mysql.connector  # pip install mysql-connector-python

# Настройка логирования 
logging.basicConfig(level=logging.INFO)

# Параметры подключения к SSH
SSH_HOST = 'ovz1.9138995941.me2jm.vps.myjino.ru'
SSH_PORT = 49262
SSH_USERNAME = 'root'
SSH_PASSWORD = 'kissibplc1313'

# Параметры подключения к MariaDB
DB_HOST = '127.0.0.1'
DB_PORT = 3306  # Порт, на который будет проброшен туннель
DB_USER = 'root'
DB_PASSWORD = 'qwe123'
DB_NAME = 'sibplc'


with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(DB_HOST, DB_PORT),
) as tunnel:
    tunnel.start()
    if tunnel.is_active:
        print("Туннель активен")
    else:
        print("Туннель не активен")

    allocated_local_port = tunnel.local_bind_port
    print(allocated_local_port)

    # Настройка логирования для mysql.connector
    logger = logging.getLogger('mysql.connector')
    logger.setLevel(logging.DEBUG)

    # Настройка обработчика вывода логов
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    connection = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=allocated_local_port,
        database=DB_NAME
    )

    print("2")
    cursor = connection.cursor()
    cursor.execute('SHOW TABLES;')
    tables = cursor.fetchall()

    if tables:
        for (table_name,) in tables:
            print(table_name)
    else:
        print("Таблицы в базе данных не найдены.")

    cursor.close()
    connection.close()
"""
