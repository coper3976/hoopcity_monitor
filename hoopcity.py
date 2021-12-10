#-*-encoding:utf8:-*-
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from discord_hooks import Webhook
import json
import urllib3
urllib3.disable_warnings()

my_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'application/json, text/javascript, */*; q=0.01'
}

print(">>> Start Parsing")
resp = requests.get('https://www.hoopcity.co.kr/goods/goods_search.php?keyword=%EC%A1%B0%EB%8D%98&key=goodsSearchWord&recentCount=10', headers=my_header)
resp.encoding = ''
bs = BeautifulSoup(resp.text, 'lxml')
divs = bs.find_all('div', class_='item_cont')

for div in divs:
    title = div.find('strong', class_='item_name').text.strip()
    productLink = 'https://www.hoopcity.co.kr' + div.find('a', class_='')['href']
    imgLink = div.find('div', class_='item_photo_box').img['src'].strip().replace('(1)', '')
    price = div.find('strong', class_='item_price').text.strip()

if __name__ == "__main__":
    ''' --------------------------------- Main --------------------------------- '''
    MONITOR_DELAY = 5
    # 기존 상품정보 가져오기
    print("DB 생성중...")
    resp = requests.get('https://www.hoopcity.co.kr/goods/goods_search.php?keyword=%EC%A1%B0%EB%8D%98&key=goodsSearchWord&recentCount=10', headers=my_header)
    resp.encoding = ''
    bs = BeautifulSoup(resp.text, 'lxml')
    divs = bs.find_all('div', class_='item_cont')
    product_db = dict()

    for div in divs:
        title = div.find('strong', class_='item_name').text.strip()
        productLink = 'https://www.hoopcity.co.kr' + div.find('a', class_='')['href']
        imgLink = div.find('div', class_='item_photo_box').img['src'].strip().replace('(1)', '')
        price = div.find('strong', class_='item_price').text.strip()
        product_db[title] = [title, price, imgLink, productLink] 

    #테스트
    product_db.pop('JORDAN ZOOM SEPAREATE PF')

    #모니터링 시작
    print("<모니터링 시작>")
    for loopCnt in tqdm(range(int(1))):
        resp = requests.get('https://www.hoopcity.co.kr/goods/goods_search.php?keyword=%EC%A1%B0%EB%8D%98&key=goodsSearchWord&recentCount=10', headers=my_header)
        resp.encoding = ''
        bs = BeautifulSoup(resp.text, 'lxml')
        divs = bs.find_all('div', class_='item_cont')

        for div in divs:
            title = div.find('strong', class_='item_name').text.strip()
            productLink = 'https://www.hoopcity.co.kr' + div.find('a', class_='')['href']
            imgLink = div.find('div', class_='item_photo_box').img['src'].strip().replace('(1)', '')
            price = div.find('strong', class_='item_price').text.strip()

            product_db[4] = [title, price, imgLink, productLink] 
             
            if title not in product_db.keys():
                product_db[title] = [title, price, imgLink, productLink]
                print("제품명 :", title, "가격 :", price, "제품 링크 :", productLink, "제품 사진 :", imgLink)
        time.sleep(MONITOR_DELAY)
