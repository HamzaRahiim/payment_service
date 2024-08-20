import json
import logging
from aiokafka import AIOKafkaConsumer
from payment import payment_pb2
from payment.kafka.schema_registry import protobuf_deserializer
from payment.crud.payment_crud import add_new_payment, get_payment_by_id
from payment.db import get_session
from payment.model import Payment, PaymentStatus
from confluent_kafka.serialization import SerializationContext, MessageField, StringDeserializer
from payment import setting
logger = logging.getLogger(__name__)  # Configure logging appropriately
string_deserializer = StringDeserializer('utf8')


async def consume_payment_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment",
        auto_offset_reset="earliest",
        key_deserializer=lambda v: string_deserializer(v),
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(setting.KAFKA_PAYMENT_TOPIC, MessageField.VALUE))
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")
            print(f"Message value: {message.value}")
            payment_data = message.value
            status_name = payment_pb2.PaymentStatus.Name(payment_data.status)
            payment_dict = {
                "created_at": payment_data.created_at,
                "card_num": payment_data.card_num,
                "cvv": payment_data.cvv,
                "valid_thru_month": payment_data.valid_thru_month,
                "valid_thru_year": payment_data.valid_thru_year,
                "total_price": payment_data.total_price,
                "status": status_name,
            }

            with next(get_session()) as session:
                add_new_payment(
                    payment_data=Payment(**payment_dict), session=session)
    except Exception as e:
        logger.error(f"Error processing message in Consumer: {e}")
    finally:
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
