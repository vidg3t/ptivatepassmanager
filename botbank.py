import telebot#Начало работы бота
import sqlite3#Импорт баз данных
import random#id creator

db = sqlite3.connect("bank_data.db")
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    balance INT,
    telegramid BIGINT
)''')

db.commit()


bot = telebot.TeleBot("1802662040:AAHjKKxFIlZjXLlFME28QZ0sGn2BFxm-LUs")
@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda m:True)
def vhod(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    bot.send_message(message.chat.id,"menu")
    
    sql.execute(f"SELECT telegramid FROM users WHERE telegramid = {int(message.from_user.id)}")

    db.commit()
    if sql.fetchone() is None:
       #sql.execute(f"INSERT INTO users VALUES (?,?,?)", (user_login, user_password, 0))
        bot.send_message(message.chat.id,"Ваш ID не найден, хотите ли вы зарегистрироваться")
        bot.send_message(message.chat.id,"Сейчас начнется регистрация, придумайте и напишите логин, который будет использоваться при отправке денег")
        bot.register_next_step_handler(message, reg)
    else:
        bot.send_message(message.chat.id,"Введите 1 для перевода, введите 2 для просмотра баланса, введите 3 для просмотра своих данных")
        bot.register_next_step_handler(message, handle_txt)

    #for i in range(len(a)):
        



        #a[i] = list(a[i].split())
        #a[i][3] = int(a[i][3])
        #a[i][4] = int(a[i][4])
        #a[i][5] = float(a[i][5])
    
def handle_txt(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()    
    if message.text=="1":
        bot.send_message(message.chat.id,"Перевод")
        bot.send_message(message.chat.id,"Введите логин человека и сумму через пробел")
        bot.register_next_step_handler(message, trade)
    if message.text=="2":
        for b in sql.execute(f"SELECT balance FROM users WHERE telegramid = {message.from_user.id}"):
            owner_balance = b
            owner_balance = int(owner_balance[0])
            bot.send_message(message.chat.id,f"Ваш баланс на данный момент : {owner_balance}, введите любой символ для продолжения")
    if message.text=="3":
        for b in sql.execute(f"SELECT * FROM users WHERE telegramid = {message.from_user.id}"):
            bot.send_message(message.chat.id,f"Ваш логин : {b[0]}")
    #if message.text=="4":
        #f=open("info.txt","r")
        #a=f.read()
        #bot.send_message(message.chat.id,a)
def trade(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y=message.text
    y=list(y.split())
    if len(y)==2:
        target_login=y[0]
        summ=y[1]
        for i in sql.execute(f"SELECT balance FROM users WHERE login = '{target_login}'"):
            target_balance = i
            target_balance = int(target_balance[0])
        for b in sql.execute(f"SELECT balance FROM users WHERE telegramid = {message.from_user.id}"):
            owner_balance = b
            owner_balance = int(owner_balance[0])            
        if owner_balance > int(summ):
            sql.execute(f"UPDATE users SET balance = {owner_balance-int(summ)} WHERE telegramid = {message.from_user.id}")
            db.commit()
            sql.execute(f"UPDATE users SET balance = {target_balance+int(summ)} WHERE login = '{target_login}'")
            db.commit()
            bot.send_message(message.chat.id,"Проведено успешно, нажмите любую клавишу")
        else:
            bot.send_message(message.chat.id,"Недостаточно денег на счету")
def reg(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y=message.text
    sql.execute(f"INSERT INTO users VALUES(?,?,?)",(y,0,int(message.from_user.id)))
    db.commit()
    bot.send_message(message.chat.id,"Проведено успешно, нажмите любую клавишу")


bot.polling(none_stop=True, interval=0)
