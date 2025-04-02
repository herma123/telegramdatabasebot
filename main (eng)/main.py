from telebot import TeleBot, types
import buttons, server, ast, os
bot = TeleBot("")



@bot.message_handler(commands=['start'])
def start_message(message):
	create_database = types.ReplyKeyboardMarkup(resize_keyboard=True)
	create_database.add(buttons.create_database)
	server.appendKey("__users__", message.from_user.id, {"last_message": 0})
	bot.reply_to(message, "Hi, this is a bot for creating your own database.", reply_markup=create_database)

@bot.message_handler(content_types=['text'])
def message(message):
	edit_database = types.ReplyKeyboardMarkup(resize_keyboard=True)
	edit_database.add(buttons.append_key); edit_database.add(buttons.remove_key); edit_database.add(buttons.check_data); edit_database.add(buttons.clear_data)
	if message.text == "Create a new database":
		server.appendKey("__users__", message.from_user.id, {"last_message": 1})
		try: server.__read__(f"{message.from_user.id}")
		except: server.createData(f"{message.from_user.id}"); bot.reply_to(message, "You have successfully made a database", reply_markup=edit_database)
		finally: bot.reply_to(message, "You have a database. At the bottom, on the bot keyboard, you have commands to add/remove an item. Try each one!", reply_markup=edit_database)
	
	elif message.text == "Add an item to the database":
		try: 
			if os.path.getsize(f"{message.from_user.id}.json") <= 1048576:
				server.__read__(f"{message.from_user.id}"); bot.reply_to(message, "Enter the name of the item", reply_markup=types.ReplyKeyboardRemove()); server.appendKey("__users__", message.from_user.id, {"last_message": 3})
			else: bot.reply_to(message, "Your database seems to have too much weight ( no more than 1 megabyte ). Try clearing it completely, or removing a couple of items", reply_markup = edit_database) 
		except: bot.reply_to(message, "First you need to create a database. Write /start for more details")

	elif message.text == "Delete an item from the database":
		try:server.__read__(f"{message.from_user.id}"); bot.reply_to(message, "Enter the name of the item", reply_markup=types.ReplyKeyboardRemove()); server.appendKey("__users__", message.from_user.id, {"last_message": 5})
		except:bot.reply_to(message, "First you need to create a database. Write /start for more details")

	elif message.text == "Clear the database":
		try: server.__read__(f"{message.from_user.id}"); server.removeKeys(f"{message.from_user.id}"); bot.reply_to(message, "You have cleared the database of all items")
		except: bot.reply_to(message, "First you need to create a database. Write /start for more details")

	elif message.text == "View the contents of the database":
		try: server.__read__(f"{message.from_user.id}")
		except: bot.reply_to(message, "First you need to create a database. Write /start for more details")
		else: 
			server.__read__(f"{message.from_user.id}"); bot.send_document(message.chat.id, open(f"{message.from_user.id}.json", "rb")); 
			with open(f"{message.from_user.id}.txt", "w+") as data: data.write(f"{server.__read__(message.from_user.id)}")
			bot.send_document(message.chat.id, open(f"{message.from_user.id}.txt", "rb"))
		
	else:
		if server.getKey("__users__", message.from_user.id)["last_message"] == 3:
			bot.reply_to(message, """Now enter the value of the element. (You can write the value of different types - str, int, float, turple, dict, list, bool).\n\nYou can also write ordinary numbers: 1 or 123 or -213 or 2.4 or -2.4\n\nTo write a string, you must put the value in quotes, i.e.: "Egor" or 'Daniel'\n\nIn a list/dictionary/cortex, you must put inverted commas to write a string.\n\nFor example:   ['Moscow'] or ('New York', "Chicago") or {"Capitals": ['Moscow', 'Washington', "Paris", 'London']}\n\nThere are also records of Boolean values such as True or False.""")
			server.appendKey("__users__", message.from_user.id, {"last_message": 4, "name_element": message.text})

		elif server.getKey("__users__", message.from_user.id)["last_message"] == 4:
			try: server.appendKey(f"{message.from_user.id}", server.getKey("__users__", message.from_user.id)["name_element"], ast.literal_eval(message.text)); bot.reply_to(message, "You have successfully made a new item in your database. To view the database, click on the ‘View database contents’ button", reply_markup=edit_database); server.appendKey("__users__", message.from_user.id, {"last_message": 0})
			except: bot.reply_to(message, "Most likely, you made a mistake in writing the value for the element. Please read the top message carefully.", reply_markup=edit_database); server.appendKey("__users__", message.from_user.id, {"last_message": 0})

		elif server.getKey("__users__", message.from_user.id)["last_message"] == 5:
			try: server.removeKey(f"{message.from_user.id}", message.text); bot.reply_to(message, f"You have successfully deleted an element '{message.text}'", reply_markup=edit_database)
			except: bot.reply_to(message, "This item does not exist in your database", reply_markup=edit_database)
			server.appendKey("__users__", message.from_user.id, {"last_message": 0})
			

bot.infinity_polling()