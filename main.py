from telegram.ext import Updater, CommandHandler
from loguru import logger

from settings import API_TOKEN, POSTGRES_USER,  POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRESQL_HOST, \
    PARSE_URL, config
from apps.utils import PostgresDB, parse_url
from text_data import *


logger.configure(**config)
psg_bd = PostgresDB(POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRESQL_HOST, POSTGRES_PORT)


def start(update, context):
    """/start"""
    logger.info(f'{update.message.from_user.first_name} присоединился')
    return update.message.reply_text(TEXT_START_HELLO_PRIVATE_CHAT.format(update.message.from_user.first_name,
                                                                          update.message.from_user.username))


def help_command(update, context):
    """/help"""
    update.message.reply_text('Help!')
    return update.message.reply_text(HELP_TEXT)


def lastnews(update, context):
    """Последняя новость"""
    last_news = psg_bd.execute('last_news_all.sql', select=True)
    if last_news:
        return update.message.reply_text(f'title: {last_news[0][1]}\n'
                                         f'url: {last_news[0][2]}\n'
                                         f'date: {last_news[0][3]}\n')
    return update.message.reply_text(EMPTY_TEXT)


def firstnews(update, context):
    """Первая новость"""
    first_news = psg_bd.execute('first_news_all.sql', select=True)
    if first_news:
        return update.message.reply_text(f'title: {first_news[0][1]}\n'
                                         f'url: {first_news[0][2]}\n'
                                         f'date: {first_news[0][3]}\n')
    return update.message.reply_text(EMPTY_TEXT)


def listnews(update, context):
    """Список новостей"""
    all_news = psg_bd.execute('select_all_news.sql', select=True)
    message = ''
    if all_news:
        for i, news in enumerate(all_news):
            message += f'{i + 1}. title: {news[0]} date: {news[1]}\n'
        return update.message.reply_text(message)
    return update.message.reply_text(EMPTY_TEXT)


def get_news(context):
    """Получение новостей с сайтом посредством силами самого бота"""
    list_news = parse_url(PARSE_URL)
    list_news.reverse()
    logger.info(f'Спарсили {len(list_news)} новость/ей')

    last_news = psg_bd.execute('last_news.sql', select=True)
    index = 0

    if last_news:
        last_news_title = last_news[0][0]
        for i, news in enumerate(list_news):
            if news[0] == last_news_title:
                index = i
                break

    if index > 0:
        list_news = list_news[index + 1:]
    if list_news or not last_news:
        logger.info(f'Добавили в БД {len(list_news)} новость/ей')
        psg_bd.execute('insert_news.sql', commit=True, data=list_news)


def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("lastnews", lastnews))
    dp.add_handler(CommandHandler("firstnews", firstnews))
    dp.add_handler(CommandHandler("listnews", listnews))

    dp.job_queue.run_repeating(get_news, 100)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
