from typing import List, Optional
from pydantic import field_validator, validator
from sqlmodel import Field, SQLModel, Relationship, Enum
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "successful"
    FAILED = "failed"
    DECLINE = "declined"
    COD = "cash_on_delivery"


class PaymentBase(SQLModel):
    payment_id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    # Add a custom JSON encoder for datetime fields

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()  # Convert datetime to ISO format string
        }


class Payment(PaymentBase, table=True):
    card_num: int
    cvv: int
    valid_thru_month: int = Field(ge=1, le=12)
    valid_thru_year: int = Field(ge=2024)
    total_price: float
    status: PaymentStatus


class PaymentCreate(SQLModel):
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    card_num: int
    cvv: int
    valid_thru_month: int = Field(ge=1, le=12)
    valid_thru_year: int = Field(ge=2024)
    total_price: float
    status: PaymentStatus

    @field_validator("card_num")
    def validate_card_num(cls, v):
        if len(str(v)) != 6:  # Assuming card number length should be 16 digits
            raise ValueError("Card number must be 16 digits long")
        # if not str(v).isdigit():
        #     raise ValueError("Card number must contain only digits")
        return v

    @field_validator("cvv")
    def validate_cvv(cls, v):
        if len(str(v)) != 3:  # Assuming CVV length should be 3 digits
            raise ValueError("CVV must be 3 digits long")
        return v


class PaymentResponse (PaymentBase, SQLModel):
    total_price: float
    status: PaymentStatus


class PaymentKafkaResponse (SQLModel):
    payment_id: int
