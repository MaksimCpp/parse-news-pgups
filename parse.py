import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def check_char(ch: chr) -> bool:
    """
    Проверка является ли символ специальным знаком
    Возвращает буллевое значение
    """
    return ch.isalnum() or ch == " " or ch == "\n"


def download_image(folder_name: str, image_tag) -> bool:
    """
    Скачивает картинки новости
    Если всё хорошо, возвращает True
    """
    try:
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

        return True

    except Exception:
        return False


def parse_text_news(url: str) -> bool:
    """
    Парсит и печатает длиный текст новости
    Если всё хорошо, возвращает True
    """
    response = requests.get(url)

    if not response.ok:
        print("Ошибка запроса")
        return False

    new_soup = BeautifulSoup(response.text, 'lxml')

    # Длинный текст новости
    paragraphs = new_soup.find_all('p')
    star_index_paragraph = 1
    end_index_paragraph = len(paragraphs) - 1

    print("\nДлинный текст:")

    for index in range(star_index_paragraph, end_index_paragraph):
        text = paragraphs[index].text.strip()
        # Очистка строки от спец символов
        text = ''.join(ch for ch in text if check_char(ch))
        print(paragraphs[index].text.strip())

    # Имя папки в которую будут скачиваться картинки
    folder_name = 'images/'

    # Если папки нет создаем её
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Тег картинки-кнопки
    image_tag = new_soup.find_all('a', class_='gallery-item')
    download_image(folder_name, image_tag)

    return True


def parse_news(url: str) -> bool:
    """
    Парсит и печатает дату, заголовок и короткий текст новости
    Если всё хорошо, возвращает True
    """
    response = requests.get(url)

    if not response.ok:
        print("Ошибка запроса")
        return False

    soup = BeautifulSoup(response.text, 'lxml')
    index_news = 1

    # Заголовок новости
    title = soup.find_all('a', class_='title')[index_news].text.strip()

    # Дата новости
    date = soup.find_all('div', class_='date')[index_news].text.strip()

    # Короткий текст новости
    text = soup.find_all('div', class_='text')[index_news].text.strip()

    print(f'Заголовок: {title}\nДата: {date}\nКороткий текст:\n{text}')

    # Ссылка новой страници при нажатии на заголовок
    link = urljoin(url, soup.find_all('a', class_='title')[index_news]['href'])
    parse_text_news(link)

    return True


if __name__ == '__main__':
    url = 'https://www.pgups.ru/news'
    parse_news(url)
