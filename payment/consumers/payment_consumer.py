import json
from aiokafka import AIOKafkaConsumer
from payment.crud.payment_crud import add_new_payment
from payment.db import get_session
from payment.model import Payment
import logging

# ... (rest of your imports)

logger = logging.getLogger(__name__)  # Configure logging appropriately


async def consume_payment_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message on topic {message.topic}")
            payment_data = json.loads(message.value.decode())
            print("TYPE", (type(payment_data)))
            print(f"payment Data {payment_data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                db_insert_payment = add_new_payment(
                    payment_data=Payment(**payment_data), session=session)
                print("DB_INSERT_PAYMENT", db_insert_payment)
    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
