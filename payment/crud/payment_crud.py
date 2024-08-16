from sqlmodel import Session
from payment.model import Payment
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def add_new_payment(payment_data: Payment, session: Session):
    try:
        print("Adding payment to Database")

        # Convert the Unix timestamp to a datetime object
        payment_data.created_at = datetime.fromtimestamp(
            payment_data.created_at)

        session.add(payment_data)
        session.commit()
        session.refresh(payment_data)
        return True
    except Exception as e:
        logger.error(f"Error adding payment to database: {e}")
        session.rollback()
        return False
