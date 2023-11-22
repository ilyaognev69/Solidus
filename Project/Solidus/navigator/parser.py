#from bs4 import BeautifulSoup
#import requests
#from .models import ScrapedData
#
#def parse_website_data():
#    url = "https://pizzaroni.ru/"
#
#    headers = {
#        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.931 YaBrowser/23.9.3.931 Yowser/2.5 Safari/537.36',
#        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
#    }
#    
#    response = requests.get(url, headers=headers)
#    
#    if response.status_code == 200:
#        soup = BeautifulSoup(response.content, 'html.parser')
#        
#        titles = soup.find_all('a', class_="product-title").find_next_sibling()
#        pictures = soup.find_all('div', class_="preview").find_next_sibling()
#        prices = soup.find_all('span', class_="current-price").find_next_sibling()
#        
#        for title, picture, price in zip(titles, pictures, prices):
#            number_str = price.get_text().strip()
#            parsed_data = ScrapedData.objects.create(
#                title=title.text,
#                picture=picture['src'],
#                price=Decimal(number_str)
#            )
#            parsed_data.save()