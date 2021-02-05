FROM python:3.7

COPY . /bot_news

RUN pip install -r /bot_news/requirements.txt

WORKDIR /bot_news

CMD ["python", "main.py"]