# -*- coding: utf-8 -*-
import uvicorn
import uvloop
import os
uvloop.install()

# to run dev
os.environ['DEV_ENV'] = "True"
# docker run -p 6379:6379 -d redis redis-server --appendonly yes --requirepass 02011993
# docker run --name some-mongo -p 27017:27017  -d mongo


if __name__ == '__main__':
    uvicorn.run('app.main:app', loop='uvloop', reload=True, host='0.0.0.0', port=30000)
