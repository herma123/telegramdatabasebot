from telebot import TeleBot, types
import buttons, server, ast, os
bot = TeleBot("")



@bot.message_handler(commands=['start'])
def start_message(message):
	create_database = types.ReplyKeyboardMarkup(resize_keyboard=True)
	create_database.add(buttons.create_database)
	server.appendKey("__users__", message.from_user.id, {"last_message": 0})
	bot.reply_to(message, "Привет! Это бот для создания собственной базы данных.", reply_markup=create_database)

@bot.message_handler(content_types=['text'])
def message(message):
	edit_database = types.ReplyKeyboardMarkup(resize_keyboard=True)
	edit_database.add(buttons.append_key); edit_database.add(buttons.remove_key); edit_database.add(buttons.check_data); edit_database.add(buttons.clear_data)
	if message.text == "Создать новую базу данных":
		server.appendKey("__users__", message.from_user.id, {"last_message": 1})
		try: server.__read__(f"{message.from_user.id}")
		except: server.createData(f"{message.from_user.id}"); bot.reply_to(message, "Вы успешно сделали базу данных", reply_markup=edit_database)
		finally: bot.reply_to(message, "У вас есть база данных. Снизу, на клавиатуре бота, у вас есть команды для добавления/удаления элемента. Попробуйте каждую!", reply_markup=edit_database)
	
	elif message.text == "Добавить элемент в базу данных":
		try: 
			if os.path.getsize(f"{message.from_user.id}.json") <= 1048576:
				server.__read__(f"{message.from_user.id}"); bot.reply_to(message, "Введите название элемента", reply_markup=types.ReplyKeyboardRemove()); server.appendKey("__users__", message.from_user.id, {"last_message": 3})
			else: bot.reply_to(message, "Кажется ваша база данных имеет слишком большой вес ( не больше 1 мигабайта ). Попробуйте очистить ее полностью, или удалить пару элементов", reply_markup = edit_database) 
		except: bot.reply_to(message, "Для начала вам нужно создать базу данных. Напишите /start для подробного ознакомления")

	elif message.text == "Удалить элемент из базы данных":
		try:server.__read__(f"{message.from_user.id}"); bot.reply_to(message, "Введите название элемента", reply_markup=types.ReplyKeyboardRemove()); server.appendKey("__users__", message.from_user.id, {"last_message": 5})
		except:bot.reply_to(message, "Для начала вам нужно создать базу данных. Напишите /start для подробного ознакомления")

	elif message.text == "Очистить базу данных":
		try: server.__read__(f"{message.from_user.id}"); server.removeKeys(f"{message.from_user.id}"); bot.reply_to(message, "Вы очистили базу данных от всех элементов")
		except: bot.reply_to(message, "Для начала вам нужно создать базу данных. Напишите /start для подробного ознакомления")

	elif message.text == "Посмотреть содержимое базы данных":
		try: server.__read__(f"{message.from_user.id}")
		except: bot.reply_to(message, "Для начала вам нужно создать базу данных. Напишите /start для подробного ознакомления")
		else: 
			server.__read__(f"{message.from_user.id}"); bot.send_document(message.chat.id, open(f"{message.from_user.id}.json", "rb")); 
			with open(f"{message.from_user.id}.txt", "w+") as data: data.write(f"{server.__read__(message.from_user.id)}")
			bot.send_document(message.chat.id, open(f"{message.from_user.id}.txt", "rb"))
		
	else:
		if server.getKey("__users__", message.from_user.id)["last_message"] == 3:
			bot.reply_to(message, """А теперь введите значение элемента. (Вы можете записывать значение разных типов - str, int, float, turple, dict, list, bool).\n\nВы можете записывать и обычные числа: 1 или 123 или -213 или 2.4 или -2.4\n\nЧтобы записать строку - нужно писать значение в кавычках, то-есть: 'Егор' или "Даниил"\n\nВ списке/словаре/кортеже чтобы записать строку - нужно ставить кавычки.\n\nК примеру:   ['Москва'] или ('Нью-Йорк', 'Чикаго') или {'Столицы': ['Москва', 'Вашингтон', 'Париж', "Лондон"]}\n\nТакже есть запись и булевых значений, таких как True или False.""")
			server.appendKey("__users__", message.from_user.id, {"last_message": 4, "name_element": message.text})

		elif server.getKey("__users__", message.from_user.id)["last_message"] == 4:
			try: server.appendKey(f"{message.from_user.id}", server.getKey("__users__", message.from_user.id)["name_element"], ast.literal_eval(message.text)); bot.reply_to(message, "Вы успешно сделали новый элемент в своей базе данных. Чтобы посмотреть базу данных, нажмите на кнопку 'Посмотреть содержимое базы данных'", reply_markup=edit_database); server.appendKey("__users__", message.from_user.id, {"last_message": 0})
			except: bot.reply_to(message, "Скорее всего, вы допустили ошибку в написании значения для элемента. Внимательно прочитайте верхнее сообщение.", reply_markup=edit_database); server.appendKey("__users__", message.from_user.id, {"last_message": 0})

		elif server.getKey("__users__", message.from_user.id)["last_message"] == 5:
			try: server.removeKey(f"{message.from_user.id}", message.text); bot.reply_to(message, f"Вы успешно удалили элемент '{message.text}'", reply_markup=edit_database)
			except: bot.reply_to(message, "Такого элемента не существует в вашей базе данных", reply_markup=edit_database)
			server.appendKey("__users__", message.from_user.id, {"last_message": 0})
			

bot.infinity_polling()