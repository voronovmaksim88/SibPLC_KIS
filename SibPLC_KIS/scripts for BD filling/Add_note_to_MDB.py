import pyodbc

print(pyodbc.drivers())

row_dict = {}


conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=D:\YandexDisk\db\Data_Base_Sibplc_v13.mdb"
)

# for row in cursor.fetchall():
#   print(row)

# код ниже наполняет текстом поле Note (примечание)
with pyodbc.connect(conn_str) as cnxn:

    # Прежде всего, получим все данные
    with cnxn.cursor() as select_cursor:
        select_cursor.execute("SELECT * FROM Box")
        data = select_cursor.fetchall()

    # Теперь обработаем данные и обновим данные в БД
    with cnxn.cursor() as update_cursor:
        for row in data:
            print(row)
            print(type(row))
            print("\u001b[32mСвойства:")

            print("ID:", row.ID)
            print("Manufacturer:", row.Manufacturer)
            print("Model:", row.Model)
            print("Name:", row.Name)
            print("Vendor code:", row.Vendor_code)
            print("Note:", row.Note)
            print("Material:", row.Material)
            print("H:", row.H)
            print("W:", row.W)
            print("D:", row.D)
            print("IP:", row.IP)
            if row.Price_RUR:
                print("Price_RUR:", int(row.Price_RUR))
            if row.Price_EUR:
                print("Price_EUR:", int(row.Price_EUR))
            if row.Price_USD:
                print("Price_USD:", int(row.Price_USD))
            print("\u001b[0m")
            # row_list = row.

            # Получить ID записи
            row_id = row.ID

            # Новое значение для поля "Note"
            # new_note = row.Note + "\r\n" if row.Note is not None else ""
            # new_note = new_note + "- Материал: " + row.Material + "\r\n" + "- Высота: " + str(
            #      row.H) + "\r\n" + "- Ширина: " + str(row.W) + "\r\n" + "- Глубина: " + str(
            #      row.D) + "\r\n" + "- Cтепень защиты: ip" + str(row.IP)
            new_note = row.Note
            if not new_note:  # если вообще нет примечания
                new_note = "- Материал: " + row.Material + "\r\n" + "- Высота: " + str(
                    row.H) + "\r\n" + "- Ширина: " + str(row.W) + "\r\n" + "- Глубина: " + str(
                    row.D) + "\r\n" + "- Cтепень защиты: ip" + str(row.IP)

            if "Материал" not in new_note:
                new_note = new_note + "\r\n" + "- Материал: " + row.Material

            if "Высота" not in new_note:
                new_note = new_note + "\r\n" + "- Высота: " + str(row.H)

            if "Ширина" not in new_note:
                new_note = new_note + "\r\n" + "- Ширина: " + str(row.W)

            if "Глубина" not in new_note:
                new_note = new_note + "\r\n" + "- Глубина: " + str(row.D)

            if "Cтепень защиты" not in new_note:
                new_note = new_note + "\r\n" + "- Cтепень защиты: ip: " + str(row.IP)

            # SQL запрос на обновление поля "Note"
            params = (new_note, row_id)
            update_cursor.execute("UPDATE Box SET [Note] = ? WHERE ID = ?", params)

        cnxn.commit()
        # Сохранить изменения

cnxn.close()
