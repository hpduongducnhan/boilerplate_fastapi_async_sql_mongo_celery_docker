# To use this boilerplate
- database
    - use docker to start database. open firewall port if neccessary!
    ```
    > docker run --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=admin -e POSTGRES_DB=my_app -p 5432:5432 -d postgres
    >
    > docker run -p 3306:3306  --name some-mariadb -e MARIADB_ROOT_PASSWORD=password -e MYSQL_DATABASE=my_app -e MYSQL_USER=admin -e MYSQL_PASSWORD=password -d mariadb
    >
    > docker run --name some-mongo -p 27017:27017  -d mongo
    ```
    - use docker to start redis
    ```
    > docker run -p 6379:6379 -d redis redis-server --appendonly yes --requirepass 02011993
    ```
    - init aerich config
    ```
    aerich init -t app.database.sql.TORTOISE_ORM_CONFIG
    ```
    - init data of each app
    ```
    > aerich --app user init-db                     # sqlite3
    > aerich --app user_mariadb init-db             # mariadb
    > aerich --app user_postgresql init-db          # postgresql
    ```
    - migrate if models changed
    ```
    > aerich --app user migrate                     # sqlite3
    > aerich --app user_mariadb migrate             # mariadb
    > aerich --app user_postgresql migrate          # postgresql
    ```

- configure proxy in .env file if you need otherwise just ignore
    ```
    APP_USE_PROXY=True
    APP_PROXY_SERVER=http://proxy.server:port
    APP_NO_PROXY=localhost,127.0.0.1
    ```

- start celery worker and celery beat
    ```
    # worker
    > celery -A app worker --loglevel INFO -E

    # beat
    > celery -A app beat --loglevel INFO
    ```

- start application
    ```
    > python run_app.py
    or
    > uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
    ```

# Python - support 3.7, 3.8 only
- install on centos 7
    ```
    > sudo yum -y groupinstall "Development Tools"
    > yum install -y gcc openssl-devel bzip2-devel libffi-devel make sqlite-devel
    > yum -y update
    > wget https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
    > tar -xf Python-3.
    > cd Python-3.
    > ./configure --enable-loadable-sqlite-extensions --enable-optimizations && sudo make altinstall
    ```
- install on ubuntu
    ```
    > sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    > sudo apt install -y update
    > wget https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
    > tar -xf Python-3.
    > cd Python-3.
    > ./configure --enable-loadable-sqlite-extensions --enable-optimizations && sudo make altinstall
    ```

# Celery
- start worker
    ```
    > celery -A app worker --loglevel INFO -E
    ```

# Aerich
- initialize the config file and migrations location (create aerich.ini and migrations folder at root)
    ```
    > aerich init -t app.database.sql.TORTOISE_ORM_CONFIG
    ```
- init database | generate schema | create database and table
    ```
    > aerich init-db
    ```

- init database of a app
    ```
    > aerich --app <app_name> init-db
    ```

- Update models and make migrate
    ```
    > aerich migrate --name <name_what_you_want>
    ```
- Upgrade to latest version
    ```
    > aerich upgrade
    ```
- Downgrade to specified version
    ```
    > aerich downgrade
    ```
- Show history
    ```
    > aerich heads
    ```
- Inspect db tables to TortoiseORM model
    ```
    # inspect table
    > aerich inspectdb -t

    # inspect tables of app
    > aerich --app models inspectdb

    # Inspect a specified table in the default app and redirect to models.py
    > aerich inspectdb -t user > models.py
    ```
