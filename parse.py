from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os

def parse_news(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Ошибка запроса")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Заголовок новости
    title = soup.find_all('a', class_='title')[1].text.strip()
    
    # Дата новости
    date = soup.find_all('div', class_='date')[1].text.strip()

    # Короткий текст новости
    text = soup.find_all('div', class_='text')[1].text.strip()

    print(f'Заголовок: {title}\nДата: {date}\nКороткий текст:\n{text}')
  
    # Ссылка новой страници при нажатии на заголовок
    link = urljoin(url, soup.find_all('a', class_='title')[1]['href'])
    new_response = requests.get(link)

    if new_response.status_code != 200:
        print("Ошибка запроса")
        return
        
    new_soup = BeautifulSoup(new_response.text, 'html.parser')

    # Длинный текст новости
    paragraphs = new_soup.find_all('p')

    print("\nДлинный текст:")   

    for index in range(1, len(paragraphs) - 1):
        print(paragraphs[index].text.strip())

    # Имя папки в которую будут скачиваться картинки
    folder_name = 'images/'

    # Если папки нет создаем её
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    
    # Тег картинки-кнопки 
    image_tag = new_soup.find_all('a', class_='gallery-item')

    for image in image_tag:
        # URL адрес картинки
        image_url = urljoin(url, image['href'])

        # Имя картинки берется из адреса
        image_name = os.path.join(folder_name, image_url.split('/')[-1])

        # Картинка в бинарном формате
        image_data = requests.get(image_url).content

        # Скачивание картинки
        with open(image_name, 'wb') as file:
            file.write(image_data)
        

if __name__ == '__main__':
    url = 'https://www.pgups.ru/news'
    parse_news(url)