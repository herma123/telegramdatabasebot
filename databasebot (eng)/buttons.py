from telebot import types
import ast
create_database = types.KeyboardButton(text="Create a new database")
append_key = types.KeyboardButton(text="Add an item to the database")
remove_key = types.KeyboardButton(text="Delete an item from the database")
clear_data = types.KeyboardButton(text="Clear the database")
check_data = types.KeyboardButton(text="View the contents of the database")
