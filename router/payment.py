import datetime
from typing import List, Annotated
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from payment import payment_pb2, setting
from payment.db import get_kafka_producer, get_session
from payment.model import Payment, PaymentCreate, PaymentResponse, PaymentStatus
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
    # payment_dict = {field: getattr(payment, field) for field in payment.dict()}
    # payment_json = payment.json()  # This will use the custom json_encoders you defined
    payment_protbuf = payment_pb2.PaymentCreate(
        created_at=int(datetime.datetime.now().timestamp()),
        card_num=payment.card_num,
        cvv=payment.cvv,
        valid_thru_month=payment.valid_thru_month,
        valid_thru_year=payment.valid_thru_year,
        total_price=payment.total_price,
        status=payment_pb2.PaymentStatus.PENDING
    )
    # Explicitly print each field to ensure nothing is missed
    # Serialize the message to a byte string
    serialized_payment = payment_protbuf.SerializeToString()
    print(f"Serialized data: {serialized_payment}")
    await producer.send_and_wait(setting.KAFKA_PAYMENT_TOPIC, serialized_payment)
    return payment

# # Returns all placed payments


@payment_router.get("/all/", response_model=List[PaymentResponse])
def read_payments(session: Session = Depends(get_session)):
    payments = session.exec(select(Payment)).all()
    return payments

# # Returns payment of any specific payment-id


@payment_router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, session: Session = Depends(get_session)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
