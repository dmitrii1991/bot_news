from os.path import join
import re
from typing import Optional, List
from datetime import date

import psycopg2
import requests
from bs4 import BeautifulSoup

from settings import SQL_DIR


class PostgresDB:
    """класс отвечает за работу с БД"""

    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # создаем БД при первой иниц-ции, если ее нет
        self.execute('create_datebase.sql', commit=True)

    def create_conn(self):
        """Отвечает за создание соединеия к БД"""
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return conn

    def read_sql_file(self, name_file: str) -> str:
        with open(join(SQL_DIR, name_file), mode='r') as f:
            contents = f.read()
        return contents

    def execute(self, name_file, commit: bool = False, select: bool = False, data: Optional[list] = None)\
            -> Optional[list]:
        conn = self.create_conn()
        cursor = conn.cursor()
        if not data:
            cursor.execute(self.read_sql_file(name_file))
        else:
            records_list_template = ','.join(['%s'] * len(data))
            cursor.execute(self.read_sql_file(name_file).format(records_list_template), data)
        if select:
            result = cursor.fetchall()
            conn.close()
            return result
        if commit:
            conn.commit()
        conn.close()


def convert_data_to_datetime(date_input: str) -> date:
    """Преобразование строки '1 января 2020' ->  в экземпляр datetime.date'"""
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                  'ноября', 'декабря']
    date_, month, year = date_input.split(' ')
    month = month_list.index(month) + 1
    return date(day=int(date_), month=month, year=int(year))


def parse_url(url: str) -> List[tuple]:
    """ Парсит новости с заголовками, ссылкамиЮ датами

    :param url: адрес сайта
    :return:
        [
            ...
            (название_новости, ссылка_на_новость, дата)
            ...
        ]
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='card')
    result = []

    for post in quotes:
        href = post.get('href')
        title = post.find('h5', class_='card-title').text
        title = re.sub(r'\s+', ' ', title)
        title = title[1:-2]

        response = requests.get(href)
        soup = BeautifulSoup(response.text, 'lxml')
        date = convert_data_to_datetime(soup.find('span', class_='date').text)
        result.append((title, href, date))
    return result
