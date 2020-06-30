## How to:

First run

```
poetry install

```

Start all Servers:

```
docker-compose up
```

Run reddit-fetcher:

```
poetry run fetcher
```

Run mongodb sink connector:

```
poetry run mongo_sink 
```

Run mongodb source connector:

```
poetry run mongo_source
```

# Telegram

@mdbreddit_bot or t.me/mdbreddit_bot

Run telegrambot:

```
cd reddis
docker-compose up -d
cd ..
poetry run telegram
```
