from bs4 import BeautifulSoup as bs4
from bs4.element import Tag
import requests
import re
import json
from django.core.management.base import BaseCommand
		#################################################################################################
class Command(BaseCommand):
    
	def handle(self, *args, **kwargs):
		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
				 'Sec-Fetch-Site': 'cross-site',
				 'Sec-Ch-Ua-Platform': "Windows",
				 'Sec-Fetch-Mode': 'cors',
				 'Sec-Ch-Ua':'"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"'
				 }

		url = "https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=3070"





		response = requests.get(url, headers=headers)

		#################################################################################################

		soup = bs4(response.content,'html.parser')
		self.stdout.write(f'{soup.prettify()}')

		#################################################################################################

		cookies = [
			{
				"name" : "__cf_bm",
				"value" : "E4t51Vyjq1XYk3rAqDFKM1BEf2.7GOpO5zpdy1j4YXs-1687874517-0-ASV67Uio1SzGatugLFkZdlO+POpDjo/8/PzThRB/7J8B5iHAue0KLawS3Jp+jY0CVZTfgpW8nXo8EPfzvH6X3ppLntFlrb0pr5Qq6SrkG4ch",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "__Secure-ab-group",
				"value" : "13",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "__Secure-access-token",
				"value" : "3.0.EVcXHMkbTcCTbl7vMO_Y3g.13.l8cMBQAAAABkmW0EEwNjzqN3ZWKgAICQoA..20230626125719.ysgbs3chi0IvqgUyvBJoD2NWnANm-5GI0Hztt-oZVeQ",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "__Secure-ext_xcid",
				"value" : "8eb9a97a1f1f6cc1543e1369890d1f0d",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "__Secure-refresh-token",
				"value" : "3.0.EVcXHMkbTcCTbl7vMO_Y3g.13.l8cMBQAAAABkmW0EEwNjzqN3ZWKgAICQoA..20230626125719.5uWVD2lva-THQRl_ThkD0Sa2J0xDaA_TRwJ53RDqb50",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "__Secure-user-id",
				"value" : "0",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "ADDRESSBOOKBAR_WEB_CLARIFICATION",
				"value" : "1687776521",
				"domain" : 'www.ozon.ru',
			},
			{
				"name" : "guest",
				"value" : "true",
				"domain" : 'www.ozon.ru',
			},
			{
				"name" : "is_cookies_accepted",
				"value" : "1",
				"domain" : 'www.ozon.ru',
			},
			{
				"name" : "rfuid",
				"value" : "LTE5NTAyNjU0NzAsMzUuNzM4MzI5NTkzMDkyMiwtNzcyOTcyMTEwLFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCwxNTUwMDczNDg2LFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKbGJpMVZVeUlzSW1WdUxWVlRJaXdpWlc0aVhRPT0sMCwxLDAsMjQsMjM3NDE1OTMwLC0xLDIyNzEyNjUyMCwwLDEsMSwtNDkxMjc1NTIzLElFNWxkSE5qWVhCbElFZGxZMnR2SUZkcGJqTXlJRFV1TUNBb1YybHVaRzkzY3lrZ01qQXhNREF4TURFZ1RXOTZhV3hzWVE9PSxlMzA9LDY1LDE5NDMwMDMwNTQsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywtMTQ2MTUxODEyLDE2",
				"domain" : '.ozon.ru',
			},
			{
				"name" : "xcid",
				"value" : "e43eef438294d931d472e3791140e383",
				"domain" : 'www.ozon.ru',
			},
		]

		##################################################################################################

		from selenium import webdriver
		from selenium.webdriver.chrome.options import Options as ChromeOptions
		from selenium.webdriver.firefox.options import Options as FirefoxOptions

		# эти импорты нам нужны для организации механизма ожидания формирования страницы
		# и только потом получения из нее html
		from selenium.webdriver.common.by import By
		from selenium.webdriver.support.wait import WebDriverWait
		from selenium.webdriver.support import expected_conditions as EC


		# chrome_options = ChromeOptions()
		firefox_options = FirefoxOptions()

		# данные аргументы позволяют использовать движок браузера без gui
		# chrome_options.add_argument("--headless=new")
		# 
		firefox_options.add_argument("-headless")
		# driver = webdriver.Chrome(options=chrome_options)
		driver = webdriver.Firefox(options=firefox_options)

		driver.get(url)

		####################################################################################################

		# Функция, удаляющая предыдущие cookies, подставляющая нужные и получающая конечный результат страницы
		def pageOpen(url):
			driver.delete_all_cookies()
			for cookie in cookies:
				# driver.add_cookie(cookies[8])
				driver.add_cookie(cookies[0])
				driver.add_cookie(cookies[1]) 
				driver.add_cookie(cookies[2]) 
				driver.add_cookie(cookies[4]) 
			# получаем страницу
			driver.get(url)

			try:
			  # ждем пока не появится на странице тэг с id ozonTagManagerApp
				element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ozonTagManagerApp")))
			finally:
			  # возвращаем текст страницы
				return driver.page_source


		# Функция, 
		def options_dictionary(options_list: list) -> dict:
			options_dict = {}
			for option in options_list:
				options_dict[option.split(':')[0].strip()] = option.split(':')[1].strip()
			return options_dict  

		# Функция, вылавливающая данные о картинках
		def images_dict(good_id : int, mask : str) -> dict:
			images_dictionary = []
			try:
				# ищем div у которого в атрибуте data-state есть название имени файла
				data = soup.select_one(f'div[data-state*="{mask}"]')['data-state']
				# данные представлены в json формате, так что используем это и преобразуем в словарь
				json_data = json.loads(data)
				# зная структуру json данных, находим в словаре нужные нам данные
				for link in json_data['items'][good_id]['tileImage']['items']:
					images_dictionary.append(link['image']['link'])
				return images_dictionary  
			except:
				return []

		#####################################################################################################

		def func_parse(items):
			idx = 0
			for sibling in items:
				if isinstance(sibling, Tag) and sibling.text:
					# создаем словарь, куда будем помещать все полученные данные для товара
					item = {}
					bonuses = False
					# если есть бонусы за товар, получаем их
					if (t:=sibling.div.next_sibling.next_sibling.select_one('div span > span b')):
						print(t.text)
						item['bonuses'] = t.text    
						bonuses = True
					# получаем название товара
					print(item_name := sibling.div.next_sibling.next_sibling.div.a.span.span.text) 
					item['name'] = item_name
					self.stdout.write(f'item_name')
					# получаем основную картинку предпросмотра
					img = sibling.div.a.div.div.img['src']
					item['preimage'] = img

					print(item_images := images_dict(idx, img.split('/')[-1]))
					item['images'] = item_images

					# если бонусы были, то смещаемся на один таг span
					n_child = 3 if bonuses else 2

					# вы таскиваем все options для товара
					if options:=sibling.div.next_sibling.next_sibling.select_one(f'div > span:nth-child({n_child}) span'):
						options_str = str(options)
						# вырезаем ненужные тэги
						cleaned_str =re.sub(r'<?.span>|<font color="#......">|</font>','', options_str)
						print(item_options := options_dictionary(cleaned_str.split('<br/>')))
						item['options'] = item_options
					idx += 1

					# в месте цены, html фрмируется по разному - обходим эти два варианта
					if (price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.div):
						print((price_text := price.text[:-1].replace(' ','')))
						# цена идет в кодировке, которая нам не подходит, возвращаем к человеческому виду
						item['price'] =int(price_text.encode('ascii', 'ignore'))
						# item['price'] = price_text
					elif (price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.span.span):   
						print((price_text := price.text[:-1].replace(' ','')))
						item['price'] = int(price_text.encode('ascii', 'ignore'))
						# item['price'] = price_text

					# добавляем наш товар в список товаров
					captured_data.append(item)  

		########################################################################################################

#		self.stdout.write(f'{int(captured_data[0]["price"].encode("ascii", "ignore"))}')

		########################################################################################################

#		self.stdout.write(f'{captured_data.__len__()}')

		########################################################################################################

		captured_data = []
		# search = '3070'
		search = '1050+видеокарта'
		# начальная строка
		url = f"https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={search}"
		for page in range(1,3):
			# добавляем нужную страницу к url и отправляем в функцию pageOpen на скачку
			source_text = pageOpen(f'{url}&page={page}')
			# удаляем из текста всякие комментарии, чтобы не болтались мертвым грузом. Но это не обязательно
			result=re.sub(r'<!.*?->','', source_text)
			# создаем обьект bs4, на основе скаченного html
			soup = bs4(result,'html.parser')
			# Находим нужный нам html обьект по тагу и его id - там хранятся данные о товарах
			items_body = soup.find('div', id = 'paginatorContent')
			# переходим на нужные теги
			items = items_body.div.div
			# парсим данные
			func_parse(items=items)

		driver.quit()
		self.stdout.write(f'{captured_data}')
#########################################################################################################
#
#for sibling in items:
#	if sibling.text:
#		print(sibling)
#		
#########################################################################################################
#
#for sibling in items:
#	if isinstance(sibling, Tag) and sibling.text:
#		print((sibling))
#	
#########################################################################################################
#
## Ищем запись про Бонусы
#for sibling in items:
#	if isinstance(sibling, Tag):
#		print(sibling.div.next_sibling.next_sibling.select_one('div span > span b'))
#		
#########################################################################################################
#
## Ищем Название
#for sibling in items:
#	if isinstance(sibling, Tag):
#		print(item_name := sibling.div.next_sibling.next_sibling.div.a.text) 
#		
#########################################################################################################
#
## Ищем основную картинку из предпросмотра
#for sibling in items:
#	if isinstance(sibling, Tag):
#		print(img := sibling.div.a.div.div.img['src'])
#		print(img_list := img.split('/')[-1])
#	
#########################################################################################################
#
## Ищем все картинки для товара
## images_dict(0,img_list)
#print(data := soup.select_one(f'div[data-state*="{img_list}"]')['data-state'])
#json_data = json.loads(data)
#json_data
#json_data['items'][0]['tileImage']['items']
#
#########################################################################################################
#
## Опции
#for sibling in items:
#	if isinstance(sibling, Tag):
#		print(a := sibling.div.next_sibling.next_sibling.select_one('div > span:nth-child(2) span'))
#		t_a = re.sub(r'<?.span>|<font color="#......">|</font>','', str(a))
#		print(t_a)
#		print(t_a.split('<br/>'))
#		print(item_options := options_dictionary(t_a.split('<br/>')))
#
#########################################################################################################


# из ChatGPT

#from selenium import webdriver
#from bs4 import BeautifulSoup
#import time
#
## Настройка WebDriver
#driver = webdriver.Chrome('/path/to/chromedriver')  # Укажите путь к вашему драйверу
#
## Переход на страницу
#driver.get('URL_интернет-магазина')  # Замените URL на нужный адрес
#time.sleep(5)  # Даем время для загрузки страницы
#
## Получение HTML-контента
#html = driver.page_source
#
## Парсинг HTML с помощью BeautifulSoup
#soup = BeautifulSoup(html, 'html.parser')
#products = soup.find_all('class_товара')  # Измените селектор в соответствии с HTML-структурой сайта
#
## Извлечение данных о товарах
#for product in products:
#    name = product.find('class_названия_товара').text  # Аналогично модифицируйте селектор
#    price = product.find('class_цены_товара').text  # Аналогично модифицируйте селектор
#    print(f'Товар: {name}, Цена: {price}')
#
## Закрытие браузера
#driver.quit()
