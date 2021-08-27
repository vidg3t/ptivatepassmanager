import sqlite3
import telebot
import config
from telebot import types

db = sqlite3.connect("password_data.db")
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS datas(
	site TEXT,
	mail TEXT,
	login TEXT,
	password TEXT,
	phonenumber TEXT,
	id BIGINT
)''')
db.commit()

bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda m:True)

def check(message):
	bot.send_message(message.chat.id,'Введите пароль')
	bot.register_next_step_handler(message, start)
def start(message):
	if message.text == 'Your password':
		bot.send_message(message.chat.id, 'Здарова, Георгий')
		markup = types.InlineKeyboardMarkup(row_width=1)
		global item,item2,item3,item4,item5
		markup.add(item,item2,item3,item4,item5)
		bot.send_message(message.chat.id, 'PASSWORDMANAGER', reply_markup = markup)
	else:
		bot.send_message(message.chat.id, 'Пароль неверный, попробуйте заново.')
		bot.register_next_step_handler(message, start)

@bot.callback_query_handler(func = lambda call:True)

def menu(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	global item, item2, item3, item4, item5
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(item,item2,item3,item4,item5)
	if call.message:
		if call.data == '2':
			bot.send_message(call.message.chat.id, 'Введите сайт:')
			bot.register_next_step_handler(call.message, first_record)
		if call.data == '1':
			for i in sql.execute(f"SELECT * FROM datas"):
				bot.send_message(call.message.chat.id, f'Сайт: {i[0]}\nПочта: {i[1]}\nЛогин: {i[2]}\nПароль: {i[3]}\nНомер телефона: {i[4]}\nID: {i[5]}')
			bot.send_message(call.message.chat.id, 'PASSWORDMANAGER', reply_markup = markup)
		if call.data == '3':
			bot.send_message(call.message.chat.id, 'Введите любой элемент(сайт, логин, почта, пароль)')
			bot.register_next_step_handler(call.message, find_forelement)
		if call.data == '4':
			for n in sql.execute(f"SELECT * FROM datas"):
				bot.send_message(call.message.chat.id, f'Сайт: {n[0]}\nПочта: {n[1]}\nЛогин: {n[2]}\nПароль: {n[3]}\nНомер телефона: {n[4]}\nID: {n[5]}')
			bot.send_message(call.message.chat.id, 'Введите id записи, которую хотите изменить')
			bot.register_next_step_handler(call.message, change_elementfirst)

		if call.data == '5':
			for n in sql.execute(f"SELECT * FROM datas"):
				bot.send_message(call.message.chat.id, f'Сайт: {n[0]}\nПочта: {n[1]}\nЛогин: {n[2]}\nПароль: {n[3]}\nНомер телефона: {n[4]}\nID: {n[5]}')
			bot.send_message(call.message.chat.id, 'Введите id для удаления')
			bot.register_next_step_handler(call.message, delete_record)

def delete_record(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	sql.execute(f"DELETE FROM datas WHERE id = {int(call.text)}")
	db.commit()
	bot.send_message(call.chat.id, 'Данные успешно удалены')
	for i in sql.execute(f"SELECT * FROM datas"):
		bot.send_message(call.chat.id, f'Сайт: {i[0]}\nПочта: {i[1]}\nЛогин: {i[2]}\nПароль: {i[3]}\nНомер телефона: {i[4]}\nID: {i[5]}')
	global item,item2,item3,item4,item5
	markup = types.InlineKeyboardMarkup(row_width = 1)
	markup.add(item,item2,item3,item4,item5)
	bot.send_message(call.chat.id, 'PASSWORDMANAGER', reply_markup = markup)

def change_elementfirst(call):
	global uid
	uid = call.text
	bot.send_message(call.chat.id, 'Какую именно часть вы хотите изменить(сайт, почта, логин, пароль, номер)?')
	bot.register_next_step_handler(call,change_elementsecond)


def change_elementsecond(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	global element,uid
	element = call.text
	bot.send_message(call.chat.id, f'Введите новый {element}')
	if element == 'сайт':
		element = 'site'
	if element == 'почта':
		element = 'mail'
	if element == 'логин':
		element = 'login'
	if element == 'пароль':
		element = 'password'
	if element == 'номер':
		element = 'phonenumber'
	bot.register_next_step_handler(call, change_elementthird)

def change_elementthird(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	info = call.text
	global element,uid
	sql.execute(f"UPDATE datas SET {element} = '{info}' WHERE id = {uid}")
	db.commit()
	bot.send_message(call.chat.id, 'Данные успешно заменены!')
	for i in sql.execute(f"SELECT * FROM datas WHERE id = {uid}"):
		bot.send_message(call.chat.id, f'Сайт: {i[0]}\nПочта: {i[1]}\nЛогин: {i[2]}\nПароль: {i[3]}\nНомер телефона: {i[4]}\nID: {i[5]}')
	global item,item2,item3,item4,item5
	markup = types.InlineKeyboardMarkup(row_width = 1)
	markup.add(item,item2,item3,item4,item5)
	bot.send_message(call.chat.id, 'PASSWORDMANAGER', reply_markup = markup)

def find_forelement(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	element = call.text
	for e in sql.execute(f"SELECT * FROM datas WHERE site = '{element}' OR mail = '{element}' OR login = '{element}' OR password = '{element}'"):
		bot.send_message(call.chat.id, f'Сайт: {e[0]}\nПочта: {e[1]}\nЛогин: {e[2]}\nПароль: {e[3]}\nНомер телефона: {e[4]}\nID: {e[5]}')
	global item,item2,item3,item4,item5
	markup = types.InlineKeyboardMarkup(row_width = 1)
	markup.add(item,item2,item3,item4,item5)
	bot.send_message(call.chat.id, 'Это все что мы нашли')
	bot.send_message(call.chat.id, 'PASSWORDMANAGER', reply_markup = markup)

def first_record(call):
	global site
	site = call.text
	bot.send_message(call.chat.id, 'Введите почту:')
	bot.register_next_step_handler(call, second_record)

def second_record(call):
	global mail
	mail = call.text
	bot.send_message(call.chat.id, 'Введите логин:')
	bot.register_next_step_handler(call, third_record)

def third_record(call):
	global login
	login = call.text
	bot.send_message(call.chat.id, 'Введите пароль:')
	bot.register_next_step_handler(call, fourth_record)

def fourth_record(call):
	global password
	password = call.text
	bot.send_message(call.chat.id, 'Введите номер телефона:')
	bot.register_next_step_handler(call, fifth_record)

def fifth_record(call):
	db = sqlite3.connect("password_data.db")
	sql = db.cursor()
	global phonenumber,item,item2,item3,item4,item5
	phonenumber = call.text
	counterid = 0
	sql.execute("SELECT * FROM datas")
	if sql.fetchone() is None:
		counterid = -1
	for h in sql.execute(f"SELECT * FROM datas"):
		counterid += 1
	sql.execute(f"INSERT INTO datas VALUES(?,?,?,?,?,?)", (site, mail, login, password,phonenumber,int(counterid + 1)))
	db.commit()
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(item,item2,item3,item4,item5)
	bot.send_message(call.chat.id, 'Данные успешно внесены')
	bot.send_message(call.chat.id, 'PASSWORDMANAGER', reply_markup = markup)

item = types.InlineKeyboardButton('Посмотреть всю базу',callback_data='1')
item2 = types.InlineKeyboardButton('Добавить данные',callback_data='2')
item3 = types.InlineKeyboardButton('Поиск данных',callback_data='3')
item4 = types.InlineKeyboardButton('Изменить данные',callback_data='4')
item5 = types.InlineKeyboardButton('Удалить данные',callback_data='5')
site = ''
mail = ''
login = ''
password = ''
element = ''
uid = 0
bot.polling(none_stop=True, interval=0)
