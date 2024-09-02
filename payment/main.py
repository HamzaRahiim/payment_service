import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, Annotated

from datetime import timedelta
from contextlib import asynccontextmanager

from payment import payment_pb2, setting
from payment.consumers.payment_consumer import consume_payment_messages, consume_read_payment_messages
from payment.db import create_db_and_tables, engine, get_session

from router.payment import payment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Application")

    # Create database and tables
    create_db_and_tables()
    print("Database and tables created")

    # Create the consumer tasks
    consumer_task = asyncio.create_task(consume_payment_messages(
        setting.KAFKA_PAYMENT_TOPIC, 'broker:19092'))
    consume_read_payment = asyncio.create_task(consume_read_payment_messages(
        setting.KAFKA_PAYMENT_ID_TOPIC, 'broker:19092'))
    print("Kafka consumer task created")

    try:
        # Ensure the consumer has started
        await asyncio.sleep(0)
        yield

    finally:
        # Gracefully shutdown the consumer tasks
        print("Shutting down consumer task")
        consumer_task.cancel()
        consume_read_payment.cancel()

        # Wait for the tasks to complete before exiting
        await asyncio.gather(consumer_task, consume_read_payment, return_exceptions=True)

        print("Application shutdown complete")

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Payment Service App",
    description="A simple Payment CRUD application",
    version="1.0.0",
    root_path="/payment-service",
    root_path_in_servers=True
)


app.include_router(router=payment_router)


@app.get("/", tags=["Main"])
async def root():
    return {"Message": "Payment App running :-}"}


@app.get("/health", tags=["Main"])
async def health():
    return {"Message": "This is main Page:-)"}
