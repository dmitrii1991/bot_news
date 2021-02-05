[![Python version](https://img.shields.io/badge/Python-3.7-green)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/telegram-13.0-blue)]()
[![psycopg2](https://img.shields.io/badge/psycopg2-2.8.5-blue)]()

# NEWS BOT

## Описание функционала
* Пример небольшой логики бота который:
  * Парсит сайт на наличие новых новостей на сайте с определенной частотой
  * Сохраняет новости в БД (PostgreSQL - полях (date, title, url).) 
  * Имеет примитивное логирование
  * содержит след команды
    * **/lastnews** - показывает дату, заголовок и ссылку на последнюю новость по дате.
    * **/firstnews** - показывает дату, заголовок и ссылку на самую первую новость по дате.
    * **/listnews** – показывает дату и заголовки всех новостей

## запуск
*  переименовать **test-docker-compose.yaml**  в **docker-compose.yaml** 
* задать в **docker-compose.yaml** переменную TELEGRAM_API_TOKEN (поменять пароль и логин в БД по опциональности)
```yaml
  bot_app:
    restart: always
    build:
      context: .
      dockerfile: bot.Dockerfile
    environment:
      - TELEGRAM_API_TOKEN=***
      - POSTGRESQL_HOST=bot_datebase
      - POSTGRES_DB=test
      - POSTGRES_PORT=5432
```
* запуск
```shell script
    docker-compose up
```
## фото
* [пример работы бота_1](https://yadi.sk/i/ZNFE609-ccKycw "Необязательная подсказка")
* [пример работы бота_2](https://yadi.sk/i/-Ha5Go_XP5F5qw/ "Необязательная подсказка")
