import requests
import os
from bs4 import BeautifulSoup
import time
# from proxies import return_proxy
from datetime import datetime


def create_url(page):
    return main_url if page == 1 else f'https://www.vinted.pl/catalog?search_text=buty%20relaksy&search_id=30469010868&page={page}&time=1768857866'

def convert_product(product):
    converted_product = {}
    converted_product['opis'] = ''
    converted_product['size'] = ''
    converted_product['quality'] = ''
    title = product.select_one('p[data-testid$="description-title"]')
    if not title:
        return None
    subtitle = product.select_one('p[data-testid$="--description-subtitle"]')
    subtitle_text = subtitle.get_text(strip = True) if subtitle else ""
    title = title.get_text(strip=True)
    converted_product['title'] = title
    converted_product['link'] = product.select_one('a[href*="/items/"]').get('href') 
    converted_product['price'] = product.select_one('div[data-testid$="-breakdown"] span.web_ui__Text__subtitle').get_text(strip=True)
    if '·' in subtitle_text:
        converted_product['size'] = subtitle_text.split('·')[0].strip()
        converted_product['quality'] = subtitle_text.split('·')[1].strip()
    else:
        converted_product['quality'] = subtitle_text
    converted_product['images'] = []
    for img in product.select("img"):
        url = img.get('src')
        if url.startswith('https://'):
            converted_product['images'].append(url)
    detail_productParse(converted_product)
    return converted_product



def detail_productParse(converted_product):
    resp = requests.get(converted_product['link'], headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    "Accept-Language":"pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6"
    },timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')
    desc = soup.select_one('[itemprop="description"]')

    text = desc.get_text(" ", strip=True) if desc else None
    print(text)

def save_products(folder_path,list_products,page):
    byte = 0
    path = f"./parse_vinted/{datetime.now().strftime('%Y-%m-%d')};page{page}_{datetime.now().strftime('%Y-%m-%d')};"

    folder_path.append(path)
    if not os.path.isdir(path):
        os.mkdir(path)

    for product in list_products:
        path_product = f'{path}/{product["title"]}' 

        txt_path = save_text(path_product,product)
        bytes_manipulations(txt_path)
        images_byte = save_image(path_product,product)
        byte += images_byte
    bytes.append(byte)

def save_text(path_product,product):
    if not os.path.isdir(path_product):
        os.mkdir(path_product)
    txt_path = f'{path_product}/{product["title"]}.txt'
    try:
        with open(f'{path_product}/{product["title"]}.txt', 'w', encoding='utf-8') as file:
            file.write(f"Title: {product['title']}\n")
            file.write(f"Link: {product['link']}\n")
            file.write(f"Price: {product['price']}\n")
            file.write(f"Size: {product['size']}\n")
            file.write(f"Quality: {product['quality']}\n")
        return txt_path
    except Exception as ex:
        print(ex)

def bytes_manipulations(txt_path):   
    try:
        size = os.path.getsize(txt_path)
        with open(txt_path, 'a') as file:
            file.write(f"\nBytes: {size}\n")
    except Exception as ex:
        print(ex)

def checkImage_path(path_product):
    if not os.path.isdir(f'{path_product}/images'):
        os.mkdir(f'{path_product}/images')
    return True

def save_image(path_product,product):
    checkImage_path(path_product)
    images_byte = 0
    try:
        tmp = 0
        for image in product['images']:
            tmp += 1
            resp = requests.get(image)
            resp.raise_for_status()
            with open(f'{path_product}/images/{image.split("/")[-1].split("?")[0]}', 'wb') as file:
                file.write(resp.content)
            images_byte += len(resp.content)
        return images_byte
    except Exception as ex:
        print(ex)

       
def read_history(date):
    try:
        with open('./parse_vinted/folder_path.txt', 'r', encoding='utf-8') as file:
            list_dates = []
            for line in file:
                if date in line:
                    list_dates.append(line)
            return len(list_dates)
    except Exception as ex:
        print(ex)
    
def save_parse_history(folder_path):
    try:
        with open('./parse_vinted/folder_path.txt', 'a', encoding='utf-8') as file:
            file.write(str(folder_path).strip() + '\n')
    except Exception as ex:
        print(ex)

def parse_products(url):
    # list_proxies = return_proxy()
    # print(list_proxies)
    # for p in list_proxies:

    #     proxy = {
    #         "http": f"{p}",
    #         "https": f"{p}",
    #     }
    #     try:
    resp = requests.get(url, headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    "Accept-Language":"pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6"
    },timeout=10)# proxies=proxy, timeout=10)
    # if resp.status_code in (403, 429, 503):
    #     continue
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')
    products = soup.select('div.new-item-box__container[data-testid^="product-item-id-"]')
    return products
    #     except Exception as ex:
    #         print(ex)
    # return None




if __name__ == "__main__":
    stop = False

    bytes = []
    list_products = []
    folder_path = []
    main_url = f'https://www.vinted.pl/catalog?search_text=buty%20relaksy&search_id=30469010868&page=1&time=1768857866'

    print('1-  Парс данных')
    print('2 - История парсинга')
    print('3 - Выйти')

    while stop == False:
        action = int(input("Enter number: "))
        if action == 1:
            count_page = int(input('Enter page num: '))
            print('Do you want save information? Print 1 for yes, 2 for no')
            info = int(input('Enter num: '))
            if info == 1:
                for page in range(1,count_page+1):
                    time.sleep(0.5)
                    url = create_url(page)
                    products = parse_products(url)
                    for product in products:
                        converted = convert_product(product)
                        if converted is None:
                            continue
                        list_products.append(converted)
                    bytes = save_products(folder_path,list_products, page)
                    add_history(page,bytes)
                    save_parse_history(folder_path)
                print(bytes) # [54,876,634,123,76575,234]
            else:
                for page in range(1,count_page+1):
                    time.sleep(0.5)
                    url = create_url(page)
                    products = parse_products(url)
                    for product in products:
                        converted = convert_product(product)
                        print(f"Title: {converted['title']}")
                        print(f"Link: {converted['link']}")
                        print(f"Price: {converted['price']}\n")

# [4342,4324324,542542]
        elif action == 2:
            date = input('Enter datetime: ')
            res = read_history(date)
            print(f'In this list {res} pages')
            

        elif action == 3:
            stop = True





"""
    DZ
    1 - Доработать подсчет байтов при отображении статистики
    2 - Обновить структуру записи в файл истории до следующего вида
        2026-01-30;page1_2026-01-30;654
        2026-01-30;page2_2026-01-30;6573
        2026-01-30;page3_2026-01-30;34532
    3 - Нужно углубится в парсинг, реализовать идею того, что ты именно 
    открываешь каждую страничку с продуктом, и достаешь больше информации (больше картитон, больше описания, и тд)
    и сохраняешь в выходные файлы и папки
    4 - Обновить названия для картинок
    5 - Продумать механизм, что если страничка не пришла, делать доп попытку. 
    К примеру 3 попытки, если не сработало, сохранять в отдельный файл неудачный попытки обработки и идти дальше
"""


"""
PROBLEM:
1) Не могу добавлять байты в название папки страницы
   Их нужно добавлять уже после циклов когда все байты подсчитаны, возникают трудности
2) Достаю детальное описание моего продукта, но не знаю как с ним дальше манипулировать
"""