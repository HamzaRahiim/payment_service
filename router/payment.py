import datetime
from typing import List, Annotated
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from payment import setting
from payment import payment_pb2
from payment.crud.payment_crud import get_payment_by_id
from payment.db import get_kafka_producer, get_session
from payment.model import Payment, PaymentCreate, PaymentKafkaResponse, PaymentResponse, PaymentStatus
# Import the generated Protobuf class
from payment.payment_pb2 import PaymentCreate as PaymentCreateProto
import json
payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
    responses={404: {"Description": "Not found"}}
)


@payment_router.get("/", response_model=dict)
async def root():
    return {"Message": "Payment Page running :-}"}


@payment_router.post("/pay-now/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):

    # Convert Pydantic model to Protobuf message
    print(f"Producer object in create_payment: {producer}")
 # Log the producer object for debugging
    payment_proto = PaymentCreateProto(
        # Assuming created_at is a datetime object
        created_at=int(datetime.datetime.now().timestamp()),
        card_num=payment.card_num,
        cvv=payment.cvv,
        valid_thru_month=payment.valid_thru_month,
        valid_thru_year=payment.valid_thru_year,
        total_price=payment.total_price,
        status=payment_pb2.PaymentStatus.PENDING
    )

    try:
        # Log the topic and serialized payment for debugging
        print(f"Sending to topic: {setting.KAFKA_PAYMENT_TOPIC}")
        print(f"Serialized payment: {payment_proto}")
        await producer.send_and_wait(setting.KAFKA_PAYMENT_TOPIC, payment_proto)
    except Exception as e:
        print(f"Error while sending payment to Kafka: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")
    return payment


# # Returns all placed payments


@payment_router.get("/all/", response_model=List[PaymentResponse])
def read_payments(session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments

# # Returns payment of any specific payment-id


@payment_router.get("/{payment_id}", response_model=PaymentKafkaResponse)
async def read_payment(payment_id: int, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    payment_id_json = json.dumps({"payment_id": payment_id})
    # await get_payment_by_id(payment_id_json, producer)
    await producer.send_and_wait(setting.KAFKA_PAYMENT_ID_TOPIC, payment_id_json.encode("utf-8"))
    # payment = session.get(Payment, payment_id)
    # if not payment:
    #     raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentKafkaResponse(payment_id=payment_id)
