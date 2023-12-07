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
        
        
        resp = requests.get(url=url, headers=headers)
        self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        resp = resp.json()
        products_row = resp.get('data', {}).get('products', None)
        products = []
        if products_row != None and len(products_row)>0:
            for product in products_row:
                products.append({
                    'title': product.get('name', None),
                    'product_id': product.get('id', None),
                    'old_price': float(product.get('priceU', None))/100 if product.get('priceU', None) != None else None,
                    'new_price': float(product.get('salePriceU', None))/100 if product.get('salePriceU', None) != None else None,
                    'description': None,
                    'picture_urls' : None,
                    'website': 'Wildberries',
                    'reviewRating': product.get('reviewRating', None),
                    'photo_count': None
                })
        
        
        
        
        
        def check_url(d_url):
            try:
                response = session.head(d_url, allow_redirects=True)
                if response.status_code in [200, 301, 302]:
                    return True
                else:
                    return False
            except requests.RequestException:
                return False
            
            
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
            p_id = str(products[d]['product_id'])
            l = len(p_id)
            self.stdout.write(p_id)
            for x in range(100):
                x_str = f'{x:02}'  # Форматирует число с ведущим нулём, если нужно
                d_url = f'https://basket-{x_str}.wb.ru/vol{p_id[:l-5]}/part{p_id[:l-3]}/{p_id}/images/big/1.webp'
                if check_url(d_url):
                    products[d]['picture_urls'] = [d_url]
                    self.stdout.write(f'url is {d_url}')
                    add_url(d, x_str, p_id, d_url)
                    break
        
        
        
        for d in products:
            parsed_data = Wildberries.objects.create(title=d['title'], product_id=d['product_id'], picture_urls=d['picture_urls'], old_price=d['old_price'], new_price=d['new_price'], description=d['description'], website=d["website"], reviewRating=d['reviewRating'], photo_count=d['photo_count'], category="market")
            parsed_data.save()
        
        
        