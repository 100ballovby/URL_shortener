import sqlite3
# импортируем модуль sqlite

connection = sqlite3.connect('database.db')
# подключаемся к базе

with open('schema.sql') as f:
    connection.executescript(f.read())
    # запускаем скрипт создания таблицы

connection.commit()  # применяем изменения
connection.close()  # закрываем подключение
