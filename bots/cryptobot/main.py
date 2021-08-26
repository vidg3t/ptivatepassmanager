import telebot
import pyAesCrypt
import config
import os

bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda m:True)

def get_mail(message):
	bot.send_message(message.chat.id, 'Введите пароль для шифровки и расшифровки')
	bot.register_next_step_handler(message,start_menu)

def start_menu(message):
	global passw
	passw = message.text
	bot.send_message(message.chat.id, '1. Зашифровать файл. \n2. Расшифровать файл')
	bot.register_next_step_handler(message, sys_menu)

def sys_menu(message):
	if message.text == '1':
		bot.send_message(message.chat.id, 'Введите текст для шифровки')
		bot.register_next_step_handler(message,get_texttoencrypt)
	if message.text == '2':
		bot.send_message(message.chat.id, 'Отправьте файл для расшифровки')
		bot.register_next_step_handler(message, get_filetodecrypt)

def get_filetodecrypt(message):
	try:
	    chat_id = message.chat.id

	    file_info = bot.get_file(message.document.file_id)
	    downloaded_file = bot.download_file(file_info.file_path)

	    src = '/root/bots/cryptobot/' + message.document.file_name;
	    with open(src, 'wb') as new_file:
	        new_file.write(downloaded_file)
	    global passw
	    pyAesCrypt.decryptFile('result.aes', 'result.txt' , passw)
	    res = open('result.txt', 'rb')
	    bot.send_document(message.chat.id, res)
	    os.remove('/root/bots/cryptobot/result.aes')
	    os.remove('/root/bots/cryptobot/result.txt')

	    
	except Exception as e:
	    bot.reply_to(message, e)

def get_texttoencrypt(message):
	f = open('text.txt', 'w')
	f.write(message.text)
	f.close()
	global passw
	pyAesCrypt.encryptFile('text.txt', 'result.aes', passw)
	res = open('result.aes', 'rb')
	bot.send_document(message.chat.id, res)
	res.close()
	os.remove('/root/bots/cryptobot/result.aes')
	os.remove('/root/bots/cryptobot/text.txt')


passw = ''
bot.polling(none_stop=True, interval=0)
