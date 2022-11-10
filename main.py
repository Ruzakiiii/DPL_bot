import telebot
from telebot import types
import data
from data import BotDB


bot = telebot.TeleBot("5543514920:AAHd3jDlfFKiI3tYvVKdZIf3_zqx0HekGjQ", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
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

		bot.send_message(user_id, f'Привет {d}!\n\n Отправьте нам свой номер или нажмите на "Отправить контакт"', reply_markup=markup)


		bot.register_next_step_handler(message, send_welcome, a)


	# Если user_id есть
	elif user == True:
		a = 1
		user_id = message.from_user.id

		d = message.from_user.first_name

		kb = types.ReplyKeyboardMarkup(True)

		item = types.KeyboardButton('Далее')

		kb.add(item)

		bot.send_message(user_id, f'Привет {d}! Мы рады снова Вас видеть!')
		bot.register_next_step_handler(message, send_welcome, a)


def send_welcome(message, a):
	if a == 2:
		class_db = BotDB("DPL.db")
		user_id = message.from_user.id
		first_name = message.from_user.first_name
		username = message.from_user.username
		number = message.contact.phone_number

		user = class_db.add_user(user_id, first_name, username, number)

		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')

		kb.add(Feedback, About_Us, Order)

		bot.send_message(user_id, 'HELLO WORLD! Вас приветствует компания DPL!\n \nЧто бы вы хотели сделать сначала?👇',reply_markup=kb)
		bot.register_next_step_handler(message, button)

	elif a == 1:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')

		kb.add(Feedback, About_Us, Order)

		bot.send_message(user_id, 'HELLO WORLD! Вас приветствует компания DPL!\n \nЧто бы вы хотели сделать сначала?👇', reply_markup=kb)
		bot.register_next_step_handler(message, button)

	elif a == 3:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		Feedback = types.KeyboardButton('📨 Обратная связь')
		About_Us = types.KeyboardButton('🧸 О нас')
		Order = types.KeyboardButton('🎉 Заказать')

		kb.add(Feedback, About_Us, Order)

		bot.send_message(user_id, 'Вы снова в главном меню\n \nЧто бы вы хотели сделать сначала?👇', reply_markup=kb)
		bot.register_next_step_handler(message, button)

@bot.message_handler(content_types=['text'])
def button(message):
	if message.text == '🎉 Заказать':
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)
		bot.send_message(user_id, 'Мы рады, что вы хотите сделать заказ именно у нас!\n\nОставьте информацию о себе и мы с вами свяжемся!\n\nНапишите как к Вам обращаться:', reply_markup=kb)
		bot.register_next_step_handler(message, name)

def name(message):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		imya = message.text
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)
		bot.send_message(user_id, f'Приятно с Вами познакомиться {imya}\n\nНапишите название Вашего бренда:', reply_markup=kb)
		bot.register_next_step_handler(message, company_name, imya)

def company_name(message, imya):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		next = types.KeyboardButton('Пропустить 👉')
		kb.add(go_back, next)
		company_imya = message.text

		class_db = BotDB("DPL.db")
		user_id = message.from_user.id
		phone = class_db.check_phone(user_id)
		bot.send_message(user_id, f'Вы будете записанны как {imya} из компании {company_imya}\n\nВаш номер у нас записан как {phone[0][0]}, если это ваш номер телефона, нажимайте "Пропустить 👉", если Вы хотите указать другой номер для связи, то самое время это сделать:', reply_markup=kb)
		bot.register_next_step_handler(message, phone_number, imya, company_imya)

def phone_number(message, imya, company_imya):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	elif message.text == 'Пропустить 👉':
		class_db = BotDB("DPL.db")
		user_id = message.from_user.id
		phone = class_db.check_phone(user_id)
		phone_nomer = phone[0][0]
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)
		bot.send_message(user_id, f'Вы будете записанны как {imya} из компании {company_imya}\nС номером телефона: {phone_nomer}\n\nТеперь мы ждём от Вас описание проблемы как она есть и что бы вы хотели получить в итоге:', reply_markup=kb)
		bot.register_next_step_handler(message, description, imya, company_imya, phone_nomer)

	else:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)
		go_back = types.KeyboardButton('👈 В меню')
		kb.add(go_back)
		phone_nomer = message.text
		bot.send_message(user_id, f'Вы будете записанны как {imya} из компании {company_imya}\nС номером телефона: {phone_nomer}\n\nТеперь мы ждём от Вас описание проблемы как она есть и что бы вы хотели получить в итоге:', reply_markup=kb)
		bot.register_next_step_handler(message, description, imya, company_imya, phone_nomer)

def description(message, imya, company_imya, phone_nomer):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		user_id = message.from_user.id
		kb = types.ReplyKeyboardMarkup(True)

		go_back = types.KeyboardButton('👈 В меню')
		aprove = types.KeyboardButton('✅ Подтвердить')
		kb.add(go_back, aprove)
		description_text = message.text
		bot.send_message(user_id, f'Вы будете записанны как {imya} из компании {company_imya}\nС номером телефона: {phone_nomer}\n\nВаше Т.З.:\n{description_text}\n\nЕсли Всё правильно ввели, то нажмите "✅ Подтвердить" и мы запишем Ваш запрос!', reply_markup=kb)
		bot.register_next_step_handler(message, anketa, imya, company_imya, phone_nomer, description_text)

def anketa(message, imya, company_imya, phone_nomer, description_text):
	if message.text == '👈 В меню':
		a = 3
		send_welcome(message, a)
	else:
		a = 3
		user_id = message.from_user.id

		bot.send_message(user_id, f'Ваш запрос принят! Мы с Вами свяжемся в ближайшее время!')
		class_db = BotDB("DPL.db")

		class_db.add_order(user_id, imya, company_imya, phone_nomer, description_text)
		send_welcome(message, a)


bot.polling()