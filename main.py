import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
URL = 'https://www.amazon.com.br/Placa-V%C3%ADdeo-XFX-Radeon-6600/dp/B09HHLX543'

product_html = requests.get(URL, headers={'Accept-Language':'pt-BR,pt;q=0.9,en;q=0.8',
                                          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})

soup = BeautifulSoup(product_html.text, 'lxml')
price = soup.select('div div div div div div div span span .a-offscreen')[0].getText()
product_name = soup.select('div div div div h1 span')[0].getText()
product_name = product_name.strip()
price_numbers = price.split('R$')[1]
price_numbers = price_numbers
price_float = float(price_numbers.split(',')[0].replace('.','').replace(',',''))
print (price_float)
print(product_name)
target_address = 'INSERT TARGET EMAIL ADDRESS HERE'

if price_float < 2000:
    with smtplib.SMTP('smtp.gmail.com',587) as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL, 
                to_addrs=target_address,
                msg= f'Subject: Amazon Price Alert! \n\n{product_name} is now R${price_numbers}\n{URL}'.encode('utf-8')
                )
            print('Email sent')