import asyncio

from fastapi import HTTPException
from payment import setting
from sqlmodel import SQLModel, create_engine, Session
from aiokafka import AIOKafkaProducer
from payment.kafka.schema_registry import protobuf_serializer
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer
# Kafka Producer as a dependency

from aiokafka import AIOKafkaProducer
from fastapi import HTTPException
from payment.kafka.schema_registry import protobuf_serializer

string_serializer = StringSerializer('utf8')


async def get_kafka_producer():
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers='broker:19092',
            key_serializer=string_serializer,
            value_serializer=lambda v: protobuf_serializer(
                v,
                SerializationContext(
                    "payment-events", MessageField.VALUE)
            )
        )
        await producer.start()
        print("Kafka producer connected successfully")
        yield producer

    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to connect to Kafka")

CONN_STRING: str = str(setting.DATABASE_URL)


def get_engine(CONN_STRING):
    engine = create_engine(CONN_STRING, echo=True)
    print("Engine created successfully")
    return engine


engine = get_engine(CONN_STRING=CONN_STRING)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_session_override():
    CONN_STRING: str = str(setting.TEST_DATABASE_URL)
    engine = create_engine(CONN_STRING, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
