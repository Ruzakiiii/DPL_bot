import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup

import data
from data import BotDB
import config

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.from_user.id, f'Список комманд, которыми ты можешь воспользоваться пока ограничен:\n\n/start, /help')

@bot.message_handler(commands=['start'])
def start(message):
	# Функция для проверки user_id в базе

	class_db = BotDB("DPL.db")
	user_id = message.from_user.id
	user = class_db.check_user(user_id)
	d = message.from_user.first_name

	# Если user_id нет в базе
	if user == False:
		a = 2
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

		contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
		markup.add(contact)

		bot.send_message(user_id, f'Привет {d}!\n\nОтправьте нам свой номер или нажмите на "Отправить контакт"', reply_markup=markup)

		bot.register_next_step_handler(message, company_name, a)


	# Если user_id есть
	elif user == True:
		a = 1
		user_id = message.from_user.id

		d = message.from_user.first_name

		kb = types.ReplyKeyboardMarkup(True)

		item = types.KeyboardButton('Далее')

		kb.add(item)

		bot.send_message(user_id, f'Привет {d}! Мы рады снова Вас видеть!', reply_markup=kb)
		bot.register_next_step_handler(message, send_welcome, a)






"""Регистрация"""


def company_name(message, a):
	user_id = message.from_user.id
	first_name = message.from_user.first_name
	username = message.from_user.username
	number = message.contact.phone_number

	kb = types.ReplyKeyboardMarkup(True)
	chas = types.KeyboardButton('Частное лицо')
	yur = types.KeyboardButton('Юридическое лицо')
	kb.add(chas, yur)

	bot.send_message(user_id, f'Ваше имя записанно как *{first_name}*\n\nВаш номер записан как *{number}*\n\n_Вы заказываете бот для себя или для компании?_', reply_markup=kb, parse_mode="Markdown")
	bot.register_next_step_handler(message, chas_yur, first_name, username, number, a)


def chas_yur(message, first_name, username, number, a):
	user_id = message.from_user.id

	if message.text == 'Частное лицо':
		company_name = message.text

		class_db = BotDB("DPL.db")
		user = class_db.add_user(user_id, first_name, username, number, company_name)

		bot.send_message(user_id, f'Ваше имя записанно как *{first_name}*\n\nВаш номер записан как *{number}\n\n{company_name}*', parse_mode="Markdown")
		bot.register_next_step_handler(message, send_welcome, a)

	elif message.text == 'Юридическое лицо':

		bot.send_message(user_id, f'Напишите название вашей компании:')
		bot.register_next_step_handler(message, yur, first_name, username, number, a)


def yur(message, first_name, username, number, a):
	user_id = message.from_user.id

	company_name = message.text

	class_db = BotDB("DPL.db")
	user = class_db.add_user(user_id, first_name, username, number, company_name)

	kb = types.ReplyKeyboardMarkup(True)

	next = types.KeyboardButton('Продолжить 👉')

	kb.add(next)

	bot.send_message(user_id, f'Ваше имя записанно как *{first_name}*\n\nВаш номер записан как *{number}\n\n{company_name}*\n\n_Вы успешно прошли регистрацию!_', reply_markup=kb, parse_mode="Markdown")
	bot.register_next_step_handler(message, send_welcome, a)










def send_welcome(message, a):
	if a == 2:

		user_id = message.from_user.id

		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')
		Profil = types.KeyboardButton('👤 Профиль')

		kb.add(Feedback, About_Us, Order, Profil)


		bot.send_message(user_id, '_HELLO WORLD! Вас приветствует компания DPL!_\n\n*Что бы вы хотели сделать сначала?👇*',reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, menu)

	elif a == 1:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')
		Profil = types.KeyboardButton('👤 Профиль')

		kb.add(Feedback, About_Us, Order, Profil)

		#markdown = """*bold text* _italic text_ [text](URL) """


		bot.send_message(user_id, '_HELLO WORLD! Вас приветствует компания DPL!_\n\n*Что бы вы хотели сделать сначала?*👇', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, menu)

	elif a == 3:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')
		Profil = types.KeyboardButton('👤 Профиль')

		kb.add(Feedback, About_Us, Order, Profil)

		bot.send_message(user_id, '_Вы снова в главном меню_\n\n*Что бы вы хотели сделать сначала?👇*', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, menu)

@bot.message_handler(content_types='text')
def menu(message):
	if message.text == '🎉 Заказать':
		user_id = message.from_user.id

		kb = types.ReplyKeyboardMarkup(True)
		go_back = types.KeyboardButton('👈 В меню')
		miss = types.KeyboardButton('Пропустить 👉')
		kb.add(go_back, miss)

		class_db = BotDB("DPL.db")
		phone = class_db.check_phone(user_id)
		phone_nomer = phone[0][0]

		bot.send_message(user_id, f'Мы рады, что вы хотите сделать заказ именно у нас!\nОставьте информацию о себе и мы с вами свяжемся!\n\nПри регистрации мы записали вот этот Ваш номер\n📱*+{phone_nomer[0]}{phone_nomer[1]}{phone_nomer[2]} {phone_nomer[3]}{phone_nomer[4]} {phone_nomer[5]}{phone_nomer[6]}{phone_nomer[7]} {phone_nomer[8]}{phone_nomer[9]} {phone_nomer[10]}{phone_nomer[11]}*\n\n_Если он актуален нажмите "Пропустить 👉"_\n\n*Если ваш номер указан не верно, самое время написать актуальный в любом удобном для вас формате*', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, phone_number, phone_nomer)

	elif message.text == '📨 Обратная связь':
		user_id = message.from_user.id
		bot.send_message(user_id, '📨 Обратная связь')
	elif message.text == '🧸 О нас':
		user_id = message.from_user.id
		bot.send_message(user_id, '🧸 О нас')
	elif message.text == '👤 Профиль':
		user_id = message.from_user.id

		kb = types.ReplyKeyboardMarkup(True)
		miss = types.KeyboardButton('📝 Изменить')
		orders = types.KeyboardButton('⭐ Мои заказы')
		go_back = types.KeyboardButton('👈 В меню')

		kb.add(miss, orders, go_back)

		class_db = BotDB("DPL.db")

		phone = class_db.check_phone(user_id)
		phone_nomer = phone[0][0]

		ima = class_db.check_first_name(user_id)
		imya = ima[0][0]

		c_imya = class_db.company_name(user_id)
		company_imya = c_imya[0][0]

		status_orders = class_db.company_name(user_id)
		status_order = status_orders[0][0]

		bot.send_message(user_id, f'Здравствуйте, здесь вы можете:\n_-Изменить информацию о себе_\n_-Посмотреть статус выполнения заказа_', parse_mode="Markdown")
		bot.send_message(user_id, f'Мы Вас знаем как:   *{imya}*\nВаша компания назвается:   *{company_imya}*\nВаш номер телефона:   *{phone_nomer} *\n\n_Что бы Вы хотели сделать?_', parse_mode="Markdown", reply_markup=kb)
		bot.register_next_step_handler(message, acc)







"КНОПКА ЗАКАЗАТЬ"


def phone_number(message, phone_nomer):

	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)

	elif message.text == 'Пропустить 👉':
		user_id = message.from_user.id

		kb = types.ReplyKeyboardMarkup(True)
		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)

		bot.send_message(user_id, f'*Теперь напишите Ваше тех. задание*', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, description, phone_nomer)

	else:
		user_id = message.from_user.id

		kb = types.ReplyKeyboardMarkup(True)
		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)

		phone_nomer = message.text

		bot.send_message(user_id, f'*Теперь напишите Ваше тех. задание*', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, description, phone_nomer)


def description(message, phone_nomer):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		aprove = types.KeyboardButton('✅ Подтвердить')
		kb.add(go_back, aprove)

		class_db = BotDB("DPL.db")
		user_id = message.from_user.id

		ima = class_db.check_first_name(user_id)
		imya = ima[0][0]

		c_imya = class_db.company_name(user_id)
		company_imya = c_imya[0][0]

		description_text = message.text
		bot.send_message(user_id, f'Вы будете записанны как *{imya}*\nИз компании *{company_imya}*\nС номером телефона: *{phone_nomer}*\n\nВаше Т.З.:\n*{description_text}*\n\n_Если Всё правильно ввели, то нажмите "✅ Подтвердить" и мы запишем Ваш запрос!_', reply_markup=kb, parse_mode="Markdown")
		bot.register_next_step_handler(message, anketa, phone_nomer, description_text)

def anketa(message, phone_nomer, description_text):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		class_db = BotDB("DPL.db")

		a = 3
		user_id = message.from_user.id
		sequence = class_db.sequence_number(user_id)
		len_sequence_order = len(sequence)
		id_order = f'{user_id}{len_sequence_order}'

		bot.send_message(user_id, f'_*Ваш запрос принят! Мы с Вами свяжемся в ближайшее время!*_', parse_mode="Markdown")

		class_db.add_order(user_id, id_order, phone_nomer, description_text)

		send_welcome(message, a)







"""КНОПКА ПРОФИЛЬ"""


def acc(message):

	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	elif message.text == '📝 Изменить':
		a = 3

		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)


		user_id = message.from_user.id
		bot.send_message(user_id, f'пока не готово 📝 Изменить', reply_markup=kb)
		bot.register_next_step_handler(message, send_welcome, a)
	elif message.text == '⭐ Мои заказы':
		a = 3

		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)

		user_id = message.from_user.id
		orders = ['zakaz 1', 'zakaz 2']
		for i in orders:

			markup_inline = types.InlineKeyboardMarkup()
			item_add = types.InlineKeyboardButton(text='Добавить информацию к заказу', callback_data='add')
			markup_inline.add(item_add)
			# class_db = BotDB("DPL.db")
			# user_orders = class_db.get_user_orders(user_id)
			bot.send_message(user_id, f'{i}\n', reply_markup=markup_inline)

		# bot.register_next_step_handler(message, send_welcome, a)
		# class_db = BotDB("DPL.db")
		# list_id_orders = []
		# sequence_numbers = class_db.sequence_number(user_id)
		# for i in sequence_numbers:
		# 	list_id_orders.append(i)
		# bot.send_message(user_id, f'{i for i in list_id_orders} {list_id_orders}')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):

	if call.data == 'add':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
		back = types.KeyboardButton('👈 В меню')

		markup_reply.add(back)
		bot.send_message(call.message.chat.id, 'Введите текст:', reply_markup=markup_reply)
		print(call)

		def wait(call):
			bot.register_next_step_handler(call, add_info_to_orders())

		wait(call)
	else:
		pass

def add_info_to_orders(call):
	bot.send_message(user_id, f'_*Мы дополнили Ваш заказ новой информацией*_', parse_mode="Markdown")
	# if message.text == '👈 В меню':
	# 	a = 3
	# 	send_welcome(message, a)
	# else:
	# 	user_id = message.from_user.id
	# 	bot.send_message(user_id, f'_*Мы дополнили Ваш заказ новой информацией*_', parse_mode="Markdown")

bot.polling()