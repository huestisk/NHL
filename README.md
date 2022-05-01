# NHL

Data analytics to predict the 2020-21 Playoffs

## Connecting to Postgres

Get a Postgres container image from the Docker registry (<https://hub.docker.com/_/postgres>)
```bash
docker pull postgres
```

Create the container and start it with: 
```
docker run --name nhl-postgres -e POSTGRES_PASSWORD=<password> -d -p 5432:5432 postgres
```

Possible error:
 - Must stop postgreSQL first
    1. Make sure postgreSQL in path
    2. Run: sudo -u postgres pg_ctl -D /Library/PostgreSQL/<version>/data stop

Once set up, you can start and stop the container simply with:
```
docker start nhl-postgres
```

```
docker stop nhl-postgres
```


