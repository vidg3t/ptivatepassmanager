import telebot#Начало работы бота
import sqlite3#Импорт баз данных
import random#id creator

db = sqlite3.connect("bank_data.db")
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    balance BIGINT,
    telegramid BIGINT,
    status TEXT,
    businesses TEXT
)''')
db.commit()

sql.execute('''CREATE TABLE IF NOT EXISTS works(
    work_name TEXT,
    current_workers BIGINT,
    need_workers BIGINT,
    workers_list TEXT,
    requests TEXT,
    owner TEXT,
    ownerid BIGINT
)''')

db.commit()

bot = telebot.TeleBot("1802662040:AAHjKKxFIlZjXLlFME28QZ0sGn2BFxm-LUs")
@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda m:True)


def vhod(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    bot.send_message(message.chat.id,"Добро пожаловать")
    
    sql.execute(f"SELECT telegramid FROM users WHERE telegramid = {int(message.from_user.id)}")

    db.commit()
    if sql.fetchone() is None:
       #sql.execute(f"INSERT INTO users VALUES (?,?,?)", (user_login, user_password, 0))
        bot.send_message(message.chat.id,"Вы не авторизованы. Сейчас начнется регистрация, придумайте и напишите логин, который будет использоваться при отправке денег")
        bot.register_next_step_handler(message, reg_person)
    else:
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
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
            bot.send_message(message.chat.id,f"Ваш баланс на данный момент : {owner_balance}")
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)
    if message.text=="3":
        for b in sql.execute(f"SELECT * FROM users WHERE telegramid = {message.from_user.id}"):
            bot.send_message(message.chat.id,f"Ваш логин : {b[0]}")
            if b[3] == 'h':
                bot.send_message(message.chat.id,"Ваш статус : безработный")
            if b[3] == 'b':
                bot.send_message(message.chat.id,"Ваш статус : предприниматель")
            if b[3] == 'w':
                bot.send_message(message.chat.id,"Ваш статус : работник")
            bot.send_message(message.chat.id,f"Ваш баланс : {b[1]}")
            v = list()
        for u in sql.execute(f"SELECT work_name FROM works WHERE ownerid={message.from_user.id}"):#todo
            v.append(u[0])
        bot.send_message(message.chat.id, f"Ваши бизнессы : {','.join(v)}")
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)
    #if message.text=="4":
        #f=open("info.txt","r")
        #a=f.read()
        #bot.send_message(message.chat.id,a)
    if message.text == "4":
        bot.send_message(message.chat.id, "Введите название компании и число работников.")
        bot.register_next_step_handler(message, reg_business)
    if message.text == "5":
        for a in sql.execute(f"SELECT * FROM works"):
            ifempty = 'Пока никого нет'
            if a[3] == '':
                bot.send_message(message.chat.id, f'Название бизнесса - {a[0]}\nЧисло работников - {a[1]}\nМаксимальное число работников - {a[2]}\nСписок работников - {ifempty}\nРаботодатель - {a[5]}')
            else:
                bot.send_message(message.chat.id, f'Название бизнесса - {a[0]}\nЧисло работников - {a[1]}\nМаксимальное число работников - {a[2]}\nСписок работников - {a[3]}\nРаботодатель - {a[5]}')
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)
        #bot.register_next_step_handler(message, show_businesses)
    if message.text == '6':
        bot.send_message(message.chat.id,"Введите название компании, в которую хотите устроиться")
        bot.register_next_step_handler(message, work_selection)
    if message.text == '7':
        o = list()
        bot.send_message(message.chat.id,"Введите название своей компании")
        bot.register_next_step_handler(message, show_requests)      

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
            bot.send_message(message.chat.id,"Проведено успешно!")
        else:
            bot.send_message(message.chat.id,"Недостаточно денег на счету!")
    bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
    bot.register_next_step_handler(message, handle_txt)
def reg_person(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y=message.text
    sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?)",(y,0,int(message.from_user.id),'h',''))
    db.commit()
    bot.send_message(message.chat.id,"Проведено успешно!")
    bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
    bot.register_next_step_handler(message, handle_txt)

def reg_business(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y = message.text
    y = list(y.split())
    if len(y) == 2:
        for i in sql.execute(f"SELECT login FROM users WHERE telegramid = {message.from_user.id}"):
            owner = i[0]
        sql.execute(f"INSERT INTO works VALUES(?,?,?,?,?,?,?)", (y[0], 0, int(y[1]), '', '', owner, message.from_user.id))
        db.commit()
        sql.execute(f"UPDATE users SET status = 'b' WHERE telegramid = {message.from_user.id}")
        db.commit()
        bot.send_message(message.chat.id, "Ваш бизнесс успешно зарегистрирован.")
    bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
    bot.register_next_step_handler(message, handle_txt)

def work_selection(message):
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y = message.text
    sql.execute(f"SELECT work_name FROM works WHERE work_name = '{y}'")
    if sql.fetchone() is None:
        bot.send_message(message.chat.id, "Такая компания не найдена, мы вернем вас в меню, попробуйте заново")
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)
    else:
        for l in sql.execute(f"SELECT login FROM users WHERE telegramid={message.from_user.id}"):
            login = l[0]
        requests_list = list()
        for i in sql.execute(f"SELECT requests FROM works WHERE work_name='{y}'"):
            if i[0] == '':
                continue
            else:
                requests_list.append(i[0])
                requests_list.append(',')
        
        requests_list.append(login)
        requests_list.append(',')
        requests_list = ''.join(requests_list)
        sql.execute(f"UPDATE works SET requests = '{requests_list}' WHERE work_name = '{y}'")
        db.commit()
        bot.send_message(message.chat.id, "Запрос отправлен!")
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)

def show_requests(message):#TODO
    db = sqlite3.connect("bank_data.db")
    sql = db.cursor()
    y = message.text
    sql.execute(f"SELECT owner FROM works WHERE work_name='{y}'")
    if sql.fetchone() is None:
        bot.send_message(message.chat.id, "Такого предприятия не существует")
        bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
        bot.register_next_step_handler(message, handle_txt)
    else:
        b = list()
        c = 0
        o = list()
        for i in sql.execute(f"SELECT businesses FROM users WHERE telegramid={message.from_user.id}"):
            b.append(i[0])
        for m in range(len(b)):
            if b[m] == y:
                c = 1

        if c == 1:
            for x in sql.execute(f"SELECT requests FROM works WHERE ownerid={message.from_user.id}"):
                if x[0] != '':
                    o = x[0]
            o = str(''.join(o))
            o = o.split()
            bot.send_message(message.chat.id, o)
            bot.send_message(message.chat.id,'Из списка вышеперечисленных доступных работников выберите одного, и он попадет к вам!')
            bot.register_next_step_handler(message, show_requests)
        else:
            bot.send_message(message.chat.id, 'Это предприятие не принадлежит вам!') 
            bot.send_message(message.chat.id,"Введите 1 для перевода\nВведите 2 для просмотра баланса\nВведите 3 для просмотра своих данных\nВведите 4 для того чтобы открыть свой бизнесс\nВведите 5 для того чтобы посмотреть список доступных работ\nВведите 6 для того чтобы устроиться на работу\nВведите 7 для того чтобы увидеть заявки на вашу работу(для предпринимателей)")
            bot.register_next_step_handler(message, handle_txt)



bot.polling(none_stop=True, interval=0)
