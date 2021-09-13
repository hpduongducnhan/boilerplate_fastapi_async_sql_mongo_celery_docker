# -*- coding: utf-8 -*-
from umongo.frameworks import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# print(env.APP_DB_MONGO_URI)

client = AsyncIOMotorClient(settings.APP_DB_MONGO_URI)[settings.APP_DB_MONGO_NAME]
umongo_cnx = MotorAsyncIOInstance(client)


# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://host1,host2/?replicaSet=my-replicaset-name')

# more detail in links bellow
# https://github.com/Scille/umongo
# https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
