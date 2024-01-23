import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from navigator.models import Wildberries
import json



class Command(BaseCommand):
    
	def handle(self, *args, **kwargs):

		headers = {
			'Accept':'*/*',
			'Accept-Language':'ru,en;q=0.9',
			'Connection':'keep-alive',
			'Origin':'https://www.wildberries.ru',
			'Referer':'https://www.wildberries.ru/catalog/elektronika/avtoelektronika',
			'Sec-Fetch-Dest':'empty',
			'Sec-Fetch-Mode':'cors',
			'Sec-Fetch-Site':'cross-site',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36',
			'sec-ch-ua':'^\^"Chromium^\^";v=^\^"116^\^", ^\^"Not)A;Brand^\^";v=^\^"24^\^", ^\^"YaBrowser^\^";v=^\^"23^\^"',
			'sec-ch-ua-mobile':'?0',
			'sec-ch-ua-platform':'^\^"Windows^\^"',

		}
		url = "https://catalog.wb.ru/catalog/electronic14/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat=9835&curr=rub&dest=-1186630&sort=popular&spp=27&uclusters=0"

		for page in range(1, 6):
			resp = requests.get(url=f'{url}&page={page}', headers=headers)
			self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
			resp = resp.json()
			products_row = resp.get('data', {}).get('products', None)
			products = []
			if products_row != None and len(products_row)>0:
				for product in products_row:
					products.append({
						'title': product.get('name', None),
						'slug': product.get('id', None),
						'old_price': float(product.get('priceU', None))/100 if product.get('priceU', None) != None else None,
						'price': float(product.get('salePriceU', None))/100 if product.get('salePriceU', None) != None else None,
						'description': None,
						'picture_urls' : None,
						'website': 'Wildberries',
						'reviewRating': product.get('reviewRating', None),
						'photo_count': None
					})




			def add_url(d, x_str, p_id, d_url):
				product_url = f'https://basket-{x_str}.wb.ru/vol{p_id[:l-5]}/part{p_id[:l-3]}/{p_id}/info/ru/card.json'
				product_header = {
					"sec-ch-ua": '^\^"Chromium^\^";v=^\^"116^\^", ^\^"Not)A;Brand^\^";v=^\^"24^\^", ^\^"YaBrowser^\^";v=^\^"23^\^"', 
					"Referer": f"https://www.wildberries.ru/catalog/{p_id}/detail.aspx", 
					"sec-ch-ua-mobile": "?0", 
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36", 
					"sec-ch-ua-platform": '^\^"Windows^\^"'
				}
				resp = requests.get(url=product_url, headers=product_header)
				resp = resp.json()
				description = resp.get('description', None)
				media_count = resp.get('media', {}).get('photo_count', None)
				products[d]['description'] = description
				products[d]['photo_count'] = media_count
				for x in range(2, media_count+1):
					products[d]['picture_urls'] += [d_url[:-6]+str(x)+'.webp']



			session = requests.Session()
			for d in range(len(products)):
				p_id = str(products[d]['slug'])
				l = len(p_id)
				self.stdout.write(p_id)
				if 0<=int(p_id[:l-5])<=143:
					x_str = '01' 
				elif 144<=int(p_id[:l-5])<=287:
					x_str = '02'
				elif 288<=int(p_id[:l-5])<=431:
					x_str = '03'
				elif 432<=int(p_id[:l-5])<=719:
					x_str = '04'
				elif 720<=int(p_id[:l-5])<=1007:
					x_str = '05'
				elif 1008<=int(p_id[:l-5])<=1061:
					x_str = '06'
				elif 1062<=int(p_id[:l-5])<=1115:
					x_str = '07'
				elif 1116<=int(p_id[:l-5])<=1169:
					x_str = '08'
				elif 1170<=int(p_id[:l-5])<=1313:
					x_str = '09'
				elif 1314<=int(p_id[:l-5])<=1601:
					x_str = '10'
				elif 1602<=int(p_id[:l-5])<=1655:
					x_str = '11'
				elif 1656<=int(p_id[:l-5])<=1919:
					x_str = '12'
				elif 1920<=int(p_id[:l-5])<=2045:
					x_str = '13'
				elif 2046<=int(p_id[:l-5])<=2189:
					x_str = '14'
				else:
					x_str = '15'
				d_url = f'https://basket-{x_str}.wb.ru/vol{p_id[:l-5]}/part{p_id[:l-3]}/{p_id}/images/big/1.webp'
				products[d]['picture_urls'] = [d_url]
				self.stdout.write(f'url is {d_url}')
				add_url(d, x_str, p_id, d_url)




			for d in products:
				parsed_data = Wildberries.objects.create(title=d['title'], slug=d['slug'], picture_urls=d['picture_urls'], old_price=d['old_price'], price=d['price'], description=d['description'], website=d["website"], reviewRating=d['reviewRating'], photo_count=d['photo_count'])
				parsed_data.save()
        
        
        