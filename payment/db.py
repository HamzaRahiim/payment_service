from aiokafka import AIOKafkaProducer
from sqlmodel import SQLModel, create_engine, Session
from payment import setting


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


# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
