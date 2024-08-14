

# Add a New Product to the Database
from sqlmodel import Session

from payment.model import Payment


def add_new_payment(payment_data: Payment, session: Session):
    print("Adding payment to Database")
    session.add(payment_data)
    session.commit()
    session.refresh(payment_data)
    return
