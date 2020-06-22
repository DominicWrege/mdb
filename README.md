## How to:

First run

```
poetry install

```

Start Kafka:

```
docker-compose up
```

Run consumer:

```
poetry run consumer
```

Run produzer:

```
poetry run produzer
```

TODO:

- [ ] connector config for mongodb and arangodb
- [ ] save connector config from container
- [ ] more topics comments, user
- [ ] volumne for anngodb and mongdb container
- [ ] basic auth mongo-express
