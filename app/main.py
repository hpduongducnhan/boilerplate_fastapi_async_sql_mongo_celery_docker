# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.user_sql.views import router as user_sqlite3_router
from app.user_mongo.views import router as user_mongo_router
from app.core.events import startup_events, shutdown_events
from app.core.middlewares import middlewares


# declare APP
app = FastAPI(
    on_startup=startup_events,
    on_shutdown=shutdown_events,
    middleware=middlewares,
)


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


# declare Router
app.include_router(
    user_sqlite3_router,
    prefix='/user-sql',
    tags=['user_sqlite3']
)

app.include_router(
    user_mongo_router,
    prefix='/user',
    tags=['user', 'authentication']
)

# app.include_router(
#     user_mongo_router,
#     prefix='/user-mongodb',
#     tags=['user_mongodb']
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
