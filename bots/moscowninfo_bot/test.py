import requests
from bs4 import BeautifulSoup
#weathersit = map(lambda s: s.strip(), weathersit)
url = 'https://pogoda.mail.ru/prognoz/moskva/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
weathersit = soup.find_all('div', class_='information__content__additional__item')
for w in weathersit:
	#w = list(w)
	#w = map(lambda s: s.strip(), w)
	#w = ''.join(w)
	print(w.text)
