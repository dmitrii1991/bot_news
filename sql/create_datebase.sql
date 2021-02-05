CREATE TABLE IF NOT EXISTS public.news (
	news_id serial NOT NULL,
	title VARCHAR NOT NULL,
	url VARCHAR NOT NULL,
	date_news date NOT NULL,
	PRIMARY KEY (title)
);


