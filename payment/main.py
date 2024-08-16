import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional, Annotated


from datetime import timedelta
from contextlib import asynccontextmanager

from payment import setting
from payment.consumers.payment_consumer import consume_payment_messages, consume_read_payment_messages
from payment.db import create_db_and_tables, engine, get_session

from router.payment import payment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Application")

    # Create the consumer task
    consumer_task = asyncio.create_task(consume_payment_messages(
        setting.KAFKA_PAYMENT_TOPIC, 'broker:19092'))
    consume_read_payment = asyncio.create_task(consume_read_payment_messages(
        setting.KAFKA_PAYMENT_ID_TOPIC, 'broker:19092'))
    print("Kafka consumer task created")

    # Create database and tables
    create_db_and_tables()
    print("Database and tables created")

    try:
        # Ensure the consumer has started
        await asyncio.sleep(0)  # Yield control to allow the task to start
        yield  # Now the application can start accepting requests

    finally:
        # Gracefully shutdown the consumer task
        print("Shutting down consumer task")
        consumer_task.cancel()
        consume_read_payment.cancel()

        try:
            await consumer_task
            await consume_read_payment
        except asyncio.CancelledError:
            print("Consumer task was cancelled")

        print("Application shutdown complete")


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
