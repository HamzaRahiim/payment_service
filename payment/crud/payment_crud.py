

# Add a New Product to the Database
from sqlmodel import Session

from payment.model import Payment

import logging

logger = logging.getLogger(__name__)


def add_new_payment(payment_data: Payment, session: Session):
    try:
        print("Adding payment to Database")  # Keep this for now
        session.add(payment_data)
        session.commit()
        session.refresh(payment_data)
        return True  # Indicate success
    except Exception as e:
        logger.error(f"Error adding payment to database: {e}")
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure
