import requests
from bs4 import BeautifulSoup
import telebot
bot = telebot.TeleBot("1905543477:AAFVFIBvWxANhwhOaWkvY8U6cDr55qj0-LY")
@bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda m:True)
def start(message):
	bot.send_message(message.chat.id, 'Сводка по Москве')
	url = 'https://coronavirusstat.ru/country/moskva/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	find = soup.find('span', class_='font-weight-bold text-text-dark')
	illspdtd = find.text
	illspdtd = list(illspdtd)
	illspdtd.remove('+')
	illspdtd = int(''.join(illspdtd))
	find2 = soup.find_all('span', class_='text-muted')
	l = list()
	for f in find2:
		l.append(f.text)
	illspdye = l[1]
	illspdye = list(illspdye)
	illspdye.remove('+')
	illspdye = int(''.join(illspdye))
	find3 = soup.find('span', class_='font-weight-bold text-danger')
	dtspdtd = find3.text
	dtspdtd = list(dtspdtd)
	dtspdtd.remove('+')
	dtspdtd = int(''.join(dtspdtd))
	find3 = soup.find_all('span', class_='text-muted')
	k = list()
	for v in find3:
		l.append(v.text)
	dtspdye = l[-2]
	dtspdye = list(dtspdye)
	dtspdye.remove('+')
	dtspdye = int(''.join(dtspdye))
	url = 'https://pogoda.mail.ru/prognoz/moskva/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	findweather = soup.find('div', class_='information__content__temperature')
	weather = findweather.text
	weather = list(weather)
	for i in weather:
		if i == '\n':
			weather.remove('\n')
		if i == '\t':
			weather.remove('\t')
	weather = ''.join(weather)
	bot.send_message(message.chat.id, f'Коронавирус в Москве:\n    Зараженных сегодня : {illspdtd}\n    Зараженных вчера : {illspdye}\n    Умерло сегодня : {dtspdtd}\n    Умерло вчера : {dtspdye}\nПогода в Москве:\n    Температура : {weather}')

bot.polling(none_stop=True, interval=0)
