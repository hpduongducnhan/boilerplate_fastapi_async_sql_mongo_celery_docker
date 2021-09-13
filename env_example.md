# dev.env file
- to use dev env, prepare mongodb and redis 
    - maybe use docker command like 
    ```
    > docker run -p 6379:6379 -d redis redis-server --appendonly yes --requirepass your_password
    > docker run --name some-mongo -p 27017:27017  -d mongo
    ```
```
APP_USE_PROXY=False
APP_PROXY_SERVER=http://proxy.com:80
APP_NO_PROXY=localhost,127.0.0.1

# use this in email send to customer
SERVER_NAME=your_server_name
SERVER_HOST=your_server_host

APP_PROJECT_NAME=FastApiApp
APP_SECRET_KEY=your_secret_key
APP_DEBUG=False
APP_USE_TZ=False
APP_TIMEZONE=UTC
APP_TOKEN_URL=/user/get-token

APP_MIDDLEWARE_TRUSTED_HOST=["127.0.0.1","localhost"]
APP_MIDDLEWARE_LOCAL_IPS=["127.0.0.1","localhost"]

APP_DB_MARIADB_NAME=my_app
APP_DB_MARIADB_USER=admin
APP_DB_MARIADB_PASSWORD=password
APP_DB_MARIADB_HOST=localhost
APP_DB_MARIADB_PORT=3306

APP_DB_POSTGRE_NAME=my_app
APP_DB_POSTGRE_USER=admin
APP_DB_POSTGRE_PASSWORD=password
APP_DB_POSTGRE_HOST=localhost
APP_DB_POSTGRE_PORT=5432

APP_DB_MONGO_ENABLED=True
APP_DB_MONGO_URI=mongodb://localhost:27017
APP_DB_MONGO_NAME=my_app
APP_DB_MONGO_USER=root
APP_DB_MONGO_PASSWORD=password
APP_DB_MONGO_HOST=localhost
APP_DB_MONGO_PORT=27017

APP_DB_SQLITE_PATH=sqlite://./data/sqlite3/db.sqlite3

APP_REDIS_HOST=localhost
APP_REDIS_PORT=6379
APP_REDIS_DB=1
APP_REDIS_PASSWORD=your_password

APP_TELEGRAM_BOT_TOKEN=your_token
APP_TELEGRAM_NOTIFICATION_CHANNEL=your_bot_added_to_channel_above

APP_EMAILS_ENABLED=True
APP_EMAILS_FROM_NAME=your_name
APP_EMAILS_FROM_EMAIL=your_email
APP_EMAIL_RESET_TOKEN_EXPIRE_HOURS=1

APP_SMTP_TLS=True
APP_SMTP_PORT=587
APP_SMTP_HOST=smtp.gmail.com for example if you use gmail
APP_SMTP_USER=your_gmail
APP_SMTP_PASSWORD=your_password

```


# .env file
```
#
#  ---------------------------DOCKER------------------------------------------
#
ENV_NAME_PROJECT=your_project_name
ENV_NAME_NGINX_CONT=nginx
EMV_NAME_APP_CONT=backend
ENV_NAME_REDIS_CONT=redis
ENV_NAME_MONGO_CONT=mongodb
ENV_NAME_CELERY_CONT=celery


ENV_PORT_NGINX_APP=30000
ENV_PORT_NGINX_FLOWER=3000

ENV_REDIS_PASSWORD=your_password

ENV_MONGO_ROOT_USERNAME=your_account
ENV_MONGO_ROOT_PASSWORD=your_password
ENV_MONGO_PORT=27017

# if you change this, you must change in configs/nginx/....conf
ENV_GUNICORN_BIND=unix:/fastapi_app/gunicorn.sock

#
#  -----------------------------APP-------------------------------------------
#
APP_USE_PROXY=False
APP_PROXY_SERVER=your_proxy
APP_NO_PROXY=your_no_proxy

# use this in email send to customer
SERVER_NAME=your_server_name
SERVER_HOST=your_server_host

APP_PROJECT_NAME=your_project_name
APP_SECRET_KEY=your_secret_key
APP_DEBUG=False
APP_USE_TZ=False
APP_TIMEZONE=UTC
APP_TOKEN_URL=your_url_get_jwt_token /user/get-token for example

APP_MIDDLEWARE_TRUSTED_HOST=["ip_addr","domain_name"]
APP_MIDDLEWARE_LOCAL_IPS=["127.0.0.1","localhost","ip_addr]

APP_DB_MARIADB_ENABLED=False
#APP_DB_MARIADB_NAME=your_db_name
#APP_DB_MARIADB_USER=your_account
#APP_DB_MARIADB_PASSWORD=your_password
#APP_DB_MARIADB_HOST=your_db_host
#APP_DB_MARIADB_PORT=3306

APP_DB_POSTGRE_ENABLED=False
#APP_DB_POSTGRE_NAME=your_db_name
#APP_DB_POSTGRE_USER=your_account
#APP_DB_POSTGRE_PASSWORD=your_password
#APP_DB_POSTGRE_HOST=your_db_host
#APP_DB_POSTGRE_PORT=5432

APP_DB_MONGO_ENABLED=False
APP_DB_MONGO_URI=mongodb://172.27.230.12:27017
APP_DB_MONGO_NAME=your_db_name
APP_DB_MONGO_USER=your_account
APP_DB_MONGO_PASSWORD=your_password
APP_DB_MONGO_HOST=your_db_host
APP_DB_MONGO_PORT=27017


APP_DB_SQLITE_PATH=sqlite://./data/sqlite3/db.sqlite3

APP_REDIS_HOST=your_db_host
APP_REDIS_PORT=6379
APP_REDIS_DB=1
APP_REDIS_PASSWORD=your_password

APP_TELEGRAM_BOT_TOKEN=your_token
APP_TELEGRAM_NOTIFICATION_CHANNEL=your_bot_added_to_channel_above

APP_EMAILS_ENABLED=True
APP_EMAILS_FROM_NAME=your_name
APP_EMAILS_FROM_EMAIL=your_email
APP_EMAIL_RESET_TOKEN_EXPIRE_HOURS=1

APP_SMTP_TLS=True
APP_SMTP_PORT=587
APP_SMTP_HOST=smtp.gmail.com for example if you use gmail
APP_SMTP_USER=your_gmail
APP_SMTP_PASSWORD=your_password
```
