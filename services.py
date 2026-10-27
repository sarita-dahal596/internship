
from decimal import Decimal

from sqlalchemy import update
from sqlalchemy.orm import Session

from week7_project.models import (
    User,
    Account,
    Transaction,
    Merchant
)


# Find an account belonging to the logged-in user
def get_owned_account(
    db: Session,
    user: User,
    account_id: int
):
    return db.query(Account).filter(
        Account.account_id == account_id,
        Account.user_id == user.user_id
    ).first()


# Deposit money into an account
def deposit(
    db: Session,
    user: User,
    account_id: int,
    amount: Decimal
):
    if amount <= 0:
        return None, "Amount must be greater than 0"

    account = get_owned_account(db, user, account_id)

    if account is None:
        return None, "Account not found"

    try:
        # Increase the balance in the database
        db.execute(
            update(Account)
            .where(
                Account.account_id == account_id,
                Account.user_id == user.user_id
            )
            .values(balance=Account.balance + amount)
        )

        transaction = Transaction(
            user_id=user.user_id,
            account_id=account_id,
            transaction_type="DEPOSIT",
            amount=amount
        )

        db.add(transaction)
        db.commit()
        db.refresh(account)

        return account, None

    except Exception:
        db.rollback()
        raise


# Withdraw money from an account
def withdraw(
    db: Session,
    user: User,
    account_id: int,
    amount: Decimal
):
    if amount <= 0:
        return None, "Amount must be greater than 0"

    account = get_owned_account(db, user, account_id)

    if account is None:
        return None, "Account not found"

    try:
        # Deduct only if sufficient balance is available
        result = db.execute(
            update(Account)
            .where(
                Account.account_id == account_id,
                Account.user_id == user.user_id,
                Account.balance >= amount
            )
            .values(balance=Account.balance - amount)
        )

        if result.rowcount != 1:
            db.rollback()
            return None, "Insufficient balance"

        transaction = Transaction(
            user_id=user.user_id,
            account_id=account_id,
            transaction_type="WITHDRAW",
            amount=amount
        )

        db.add(transaction)
        db.commit()
        db.refresh(account)

        return account, None

    except Exception:
        db.rollback()
        raise


# Transfer money between two accounts
def transfer(
    db: Session,
    user: User,
    from_account_id: int,
    to_account_id: int,
    amount: Decimal
):
    if amount <= 0:
        return None, "Amount must be greater than 0"

    if from_account_id == to_account_id:
        return None, "Cannot transfer to the same account"

    # Sender must own the source account
    sender = get_owned_account(
        db,
        user,
        from_account_id
    )

    if sender is None:
        return None, "Sender account not found"

    receiver = db.get(Account, to_account_id)

    if receiver is None:
        return None, "Receiver account not found"

    try:
        # Deduct sender balance only if funds are sufficient
        result = db.execute(
            update(Account)
            .where(
                Account.account_id == from_account_id,
                Account.user_id == user.user_id,
                Account.balance >= amount
            )
            .values(balance=Account.balance - amount)
        )

        if result.rowcount != 1:
            db.rollback()
            return None, "Insufficient balance"

        # Credit the receiver
        db.execute(
            update(Account)
            .where(Account.account_id == to_account_id)
            .values(balance=Account.balance + amount)
        )

        transaction = Transaction(
            user_id=user.user_id,
            account_id=from_account_id,
            transaction_type="TRANSFER",
            amount=amount,
            from_account=sender.account_number,
            to_account=receiver.account_number
        )

        db.add(transaction)

        # Commit sender debit, receiver credit and history together
        db.commit()
        db.refresh(sender)

        return sender, None

    except Exception:
        db.rollback()
        raise



# Pay a merchant using the customer's account
def payment(
    db: Session,
    user: User,
    user_id: int,
    merchant_name: str,
    amount: Decimal
):
    # Prevent payments using another user's ID
    if user.user_id != user_id:
        return None, "You cannot pay for another user"

    if amount <= 0:
        return None, "Amount must be greater than 0"

    # Find the customer's first account
    account = db.query(Account).filter(
        Account.user_id == user_id
    ).order_by(Account.account_id).first()

    if account is None:
        return None, "User account not found"

    try:
        # Deduct money only when balance is sufficient
        result = db.execute(
            update(Account)
            .where(
                Account.account_id == account.account_id,
                Account.user_id == user_id,
                Account.balance >= amount
            )
            .values(balance=Account.balance - amount)
        )

        if result.rowcount != 1:
            db.rollback()
            return None, "Insufficient balance"

        # Find merchant by name
        merchant = db.query(Merchant).filter(
            Merchant.merchant_name == merchant_name
        ).first()

        # Create merchant automatically if not found
        if merchant is None:
            merchant = Merchant(
                merchant_name=merchant_name,
                merchant_code="MER-" + __import__("uuid").uuid4().hex[:12],
                balance=Decimal("0.00")
            )

            db.add(merchant)
            db.flush()

        # Credit merchant balance
        db.execute(
            update(Merchant)
            .where(Merchant.merchant_id == merchant.merchant_id)
            .values(balance=Merchant.balance + amount)
        )

        # Save payment in transaction history
        transaction = Transaction(
            user_id=user_id,
            account_id=account.account_id,
            merchant_id=merchant.merchant_id,
            transaction_type="PAYMENT",
            amount=amount,
            from_account=account.account_number,
            to_account=merchant.merchant_name,
            status="SUCCESS"
        )

        db.add(transaction)

        # Save all changes together
        db.commit()
        db.refresh(account)

        return account, None

    except Exception:
        db.rollback()
        raise
