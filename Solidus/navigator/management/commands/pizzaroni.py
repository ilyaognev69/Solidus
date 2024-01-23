import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from navigator.models import Pizzaroni
import json

def pizzaroni(self, headers):
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

                    
                    content = div.find('div', class_='product-description').text
                    price = div.find('span', itemprop='price').text
                    website = "Pizzaroni"

                    
                    picture = url+picture
                    jobs.append({"title":title, "picture":picture, "price":price, "description":content, "website":website})
            else:
                errors.append({'url':url, 'title':'Разметка была изменена'})
        else:
            errors.append({'url':url, 'title':'Страница не отвечает'})
            self.stdout.write(f'Failed to retrieve website with status code {resp.status_code}.')
        return jobs, errors
        



class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.931 YaBrowser/23.9.3.931 Yowser/2.5 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        
    
        
        def cyrillic_to_latin(text):
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

        pizzaroni_jobs, pizzaroni_errors = pizzaroni(self, headers)
        
        
       
        
        for d in pizzaroni_jobs:
            parsed_data = Pizzaroni.objects.create(title=d['title'], picture_url=d['picture'], price=d['price'], slug=cyrillic_to_latin(d['title']), description=fix_json_string(d['description']), website=d["website"])
            parsed_data.save()