import json
from aiokafka import AIOKafkaConsumer
from payment.crud.payment_crud import add_new_payment, get_payment_by_id
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
            with next(get_session()) as session:
                add_new_payment(
                    payment_data=Payment(**payment_data), session=session)
    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


async def consume_read_payment_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment_read",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message on topic {message.topic}")
            message_data = json.loads(message.value.decode())
            payment_id = message_data.get("payment_id")
            # print(f"Received payment ID: {payment_id}")

            if payment_id is None:
                logger.error("Payment ID is missing in the message")
                continue

            with next(get_session()) as session:
                print(f"Fetching payment with ID {
                      payment_id} from the database")
                payment = get_payment_by_id(
                    payment_id=payment_id, session=session)

                if payment:
                    print(f"Payment found: {payment}")
                else:
                    print(f"Payment with ID {payment_id} not found")

    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
