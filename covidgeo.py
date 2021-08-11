import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.message import EmailMessage
import time
import schedule

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

dates = {
	12:'December',
	1:'January',
	2:'February',
	3:'March',
	4:'April',
	5:'May',
	6:'June',
	7:'July',
	8:'August',
	9:'September',
	10:'October',
	11:'November'
}

def main():
	url = 'https://www.worldometers.info/coronavirus/country/georgia/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	ills = soup.find_all('div', class_='news_body')
	names = soup.find_all('button', class_='btn btn-light date-btn')

	counter = list()
	current_datetime = datetime.now()

	form_date = f'{dates[current_datetime.month]} {current_datetime.day}'

	dater = [form_date]

	for i in ills:
		counter.append(i.text)

	for j in names:
		dater.append(j.text)

	sm = list()

	for k in range(len(counter)):
		sm.append(dater[k])
		sm.append(counter[k])
	sm = '\n'.join(sm)

	email_alert('COVID', str(sm), 'george.adl@mail.ru')

schedule.every().day.at("10:00").do(main)

while True:
	schedule.run_pending()
	time.sleep(1)