from telebot import types
import ast
create_database = types.KeyboardButton(text="Создать новую базу данных")
append_key = types.KeyboardButton(text="Добавить элемент в базу данных")
remove_key = types.KeyboardButton(text="Удалить элемент из базы данных")
clear_data = types.KeyboardButton(text="Очистить базу данных")
check_data = types.KeyboardButton(text="Посмотреть содержимое базы данных")
