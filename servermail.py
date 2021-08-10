import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

def email_alert(subject,body,to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to


    user = "saintjavatest@gmail.com"
    msg['from'] = user
    password = "mwiicqrbyccpzgrx"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def get_currency():
    url = 'https://finance.yahoo.com/quote/BTC-USD/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quote = soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
    fresh_currency = list(quote.text)
    fresh_currency.remove(',')
    #print(fresh_currency)
    leng = len(fresh_currency)
    good_currency = list()
    fresh_currency.reverse()
    h = list()
    for i in range(len(fresh_currency)):
        h.append(fresh_currency[i])
        if fresh_currency[i] == '.':
            break
    #fresh_currency.reverse()
    #print(h)
    for i in range(len(h)):
        fresh_currency.remove(h[i])
    #print(fresh_currency)
    fresh_currency.reverse()
    currency = int(''.join(fresh_currency))
    #print(y)
    return currency

prev = list()
prev.append(get_currency())
print(prev)
val = get_currency()
email_alert('btc', str(val), 'george.adl@mail.ru')
while True:
    val = get_currency()
    if val != prev[-1]:
        prev.append(val)
        email_alert('btc', str(prev), 'george.adl@mail.ru')
    print(prev)
    time.sleep(60)
