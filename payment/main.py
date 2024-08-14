import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional, Annotated


from datetime import timedelta
from contextlib import asynccontextmanager

from payment import setting
from payment.consumers.payment_consumer import consume_payment_messages
from payment.db import create_db_and_tables, engine, get_session

from router.payment import payment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Application")
    task = asyncio.create_task(consume_payment_messages(
        setting.KAFKA_PAYMENT_TOPIC, 'broker:19092'))
    print("Kafka consumer started")
    create_db_and_tables()
    print("Database and tables created")
    yield

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Payment Service App",
    description="A simple Payment CRUD application",
    version="1.0.0",
)


app.include_router(router=payment_router)


@app.get("/", tags=["Main"])
async def root():
    return {"Message": "Payment App running :-}"}
