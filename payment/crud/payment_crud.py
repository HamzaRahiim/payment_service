from sqlmodel import Session
from datetime import datetime
from payment.model import Payment
import logging

logger = logging.getLogger(__name__)


def add_new_payment(payment_data: Payment, session: Session):
    try:
        print("Adding payment to Database")  # Keep this for now
        # Convert the Unix timestamp to a datetime object
        payment_data.created_at = datetime.fromtimestamp(
            payment_data.created_at)
        session.add(payment_data)
        session.commit()
        session.refresh(payment_data)
        return True  # Indicate success
    except Exception as e:
        logger.error(f"Error adding payment to database: {e}")
        session.rollback()  # Rollback the transaction in case of error
        return False  # Indicate failure


def get_payment_by_id(payment_id: int, session: Session):
    try:
        print(f"Fetching payment with ID {
              payment_id} from Database")  # Keep this for now
        payment = session.get(Payment, payment_id)
        if not payment:
            logger.error(f"Payment with ID {payment_id} not found")
            return None  # Indicate failure (payment not found)
        return payment  # Indicate success (payment found)
    except Exception as e:
        logger.error(f"Error fetching payment with ID {payment_id}: {e}")
        return None  # Indicate failure (error occurred)
