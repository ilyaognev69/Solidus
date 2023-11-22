import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from navigator.models import Market
import json


'''def pizzaroni(self, headers):
        url = "https://pizzaroni.ru"
        resp = requests.get(url, headers=headers)
        self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        jobs = []
        errors = []
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', class_="product-list")

            if main_div:
                div_lst = main_div.find_all('div', class_='product-ajax-cont')
                for div in div_lst:
                    title = div.find('a', class_="product-title").text
                    picture = div.find('div', class_="preview")

                    a_elements = picture.find_all('a')
                    picture = a_elements[1]["href"]

                    href = div.find('a', class_='product-title')["href"]
                    content = div.find('div', class_='product-description').text
                    price = div.find('span', itemprop='price').text
                    website = "Pizzaroni"
#                        if len(content)>1:
#                            content = content[1].text
#                        else:
#                            content = "Нет описания"
                    #comp = div.find('div', class_='vacancy-serp-item_meta-info-company').find('a')
#                        if comp:
#                            company = comp.text
#                        else:
#                            company = "Компания неизвестна"

                    href = url+href
                    picture = url+picture
                    jobs.append({"title":title, "url":href, "picture":picture, "price":price, "description":content, "website":website})
            else:
                errors.append({'url':url, 'title':'Разметка была изменена'})
        else:
            errors.append({'url':url, 'title':'Страница не отвечает'})
            self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        return jobs, errors
        

        
        
        
        
def dodo(self, headers):
        url = "https://www.wildberries.ru/"
        resp = requests.get(url, headers=headers)
        h = open("word.html", "w", encoding="utf-8")
        h.write(str(resp.text))
        h.close()
        self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        jobs = []
        errors = []
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('section', id="guzhy")

            if main_div:
                div_lst = main_div.find_all('article', class_='LfZFz')
                for div in div_lst:
                    title = div.find('div', class_="bMlSHd").text
                    picture = div.find('img', class_="lazy")["src"]

                    href = div.find('div', class_="bMlSHd")["href"]
                    content = div.find('main').text
                    price = div.find('footer').text
                    price = price[3:6]
                    website = "Dodo"
#                        if len(content)>1:
#                            content = content[1].text
#                        else:
#                            content = "Нет описания"
                    #comp = div.find('div', class_='vacancy-serp-item_meta-info-company').find('a')
#                        if comp:
#                            company = comp.text
#                        else:
#                            company = "Компания неизвестна"

                    href = url+href
                    picture = url+picture
                    jobs.append({"title":title, "url":href, "picture":picture, "price":price, "description":content, "website":website})
            else:
                errors.append({'url':url, 'title':'Разметка была изменена'})
        else:
            errors.append({'url':url, 'title':'Страница не отвечает'})
            self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        return jobs, errors      '''  
    


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
        products_row = response.get('data', {}).get('products', None)
        products = []
        if products_raw != None and len(products_raw)>0:
            for product in products_raw:
                products.append({
                    'title': product.get('name', None),
                    'product_id': product.get('id', None),
                    'old_price': float(product.get('priceU', None))/100 if product.get('priceU', None) != None else None,
                    'new_price': float(product.get('salePriceU', None))/100 if product.get('salePriceU', None) != None else None,
                    'description': None,
                    'picture_urls' : None,
                    'website': 'Wildberries',
                })
        
    '''
    curl "https://basket-10.wb.ru/vol1391/part139104/139104004/info/ru/card.json" ^
  -H "sec-ch-ua: ^\^"Chromium^\^";v=^\^"116^\^", ^\^"Not)A;Brand^\^";v=^\^"24^\^", ^\^"YaBrowser^\^";v=^\^"23^\^"" ^
  -H "Referer: https://www.wildberries.ru/catalog/139104004/detail.aspx" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.660 YaBrowser/23.9.5.660 Yowser/2.5 Safari/537.36" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  --compressed
    '''
    
    
    '''
    https://basket-10.wb.ru/vol1391/part139104/139104004/images/big/1.webp
    '''
        
        '''def cyrillic_to_latin(text):
            conversion_map = {
                'а': 'a', 'б': 'b', 'в': 'v',
                'г': 'g', 'д': 'd', 'е': 'e',
                'ё': 'e', 'ж': 'zh', 'з': 'z',
                'и': 'i', 'й': 'y', 'к': 'k',
                'л': 'l', 'м': 'm', 'н': 'n',
                'о': 'o', 'п': 'p', 'р': 'r',
                'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'h', 'ц': 'ts',
                'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                'ъ': '', 'ы': 'y', 'ь': '',
                'э': 'e', 'ю': 'yu', 'я': 'ya',
                'А': 'A', 'Б': 'B', 'В': 'V',
                'Г': 'G', 'Д': 'D', 'Е': 'E',
                'Ё': 'E', 'Ж': 'Zh', 'З': 'Z',
                'И': 'I', 'Й': 'Y', 'К': 'K',
                'Л': 'L', 'М': 'M', 'Н': 'N',
                'О': 'O', 'П': 'P', 'Р': 'R',
                'С': 'S', 'Т': 'T', 'У': 'U',
                'Ф': 'F', 'Х': 'H', 'Ц': 'Ts',
                'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
                'Ъ': '', 'Ы': 'Y', 'Ь': '',
                'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
                ' ': '-'  # замена пробела на дефис
            }
            return ''.join(conversion_map.get(char, char) for char in text)
        
        
        def fix_json_string(s):

            s = s.replace('\\xa0', ' ')
            s = s.replace('\"', '\\"')

            # Замена одинарных кавычек на двойные, но игнорирование одинарных кавычек внутри строк
            in_string = False
            result = []
            for char in s:
                if char == "'" and not in_string:
                    result.append('"')
                else:
                    result.append(char)
                if char == '"' and s[max(0, len(result) - 2)] != '\\':
                    in_string = not in_string
            return ''.join(result)

        
        
        h = open("pizzaroni.json", "w", encoding='utf-8')
        h.write(str(pizzaroni_jobs))
#        h.write(str(errors))
        h.close()
        
        
        h = open("dodo.json", "w", encoding='utf-8')
        h.write(str(dodo_jobs))
#        h.write(str(errors))
        h.close()
        
        # Чтение файла
        with open('pizzaroni.json', 'r', encoding='utf-8') as file:
            file_content_pizzaroni = file.read()
            
            
        with open('dodo.json', 'r', encoding='utf-8') as file:
            file_content_dodo = file.read()
        
        # Исправление файла
        fixed_content = fix_json_string(file_content_pizzaroni)

        # Попытка преобразования исправленной строки в JSON
        data = json.loads(fixed_content)
        
        fixed_content = fix_json_string(file_content_dodo)

        # Попытка преобразования исправленной строки в JSON
        data += json.loads(fixed_content)
        
        for d in data:
            parsed_data = Pizza.objects.create(title=d['title'], picture_url=d['picture'], price=d['price'], url=d['url'], slug=cyrillic_to_latin(d['title']), description=d['description'], website=d["website"])
            parsed_data.save()'''