from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository

def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db=db, user_id=current_user.id)
        return {"total_balance": sum([wallet.balance for wallet in wallets])}

    if not wallets_repository.is_wallet_exist(db=db, user_id=current_user.id, wallet_name=wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")

    wallet = wallets_repository.get_wallet_balance_by_name(db=db, user_id=current_user.id, wallet_name=wallet_name)
    return {"wallet": wallet_name, "balance": wallet.balance}



def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(db=db, user_id=current_user.id, wallet_name=wallet.name):
        raise HTTPException(status_code=400, detail=f"Wallet '{wallet.name}' already exists")

    wallet = wallets_repository.create_wallet(db=db, user_id=current_user.id, wallet_name=wallet.name, amount=wallet.initial_balance)
    db.commit()
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": wallet.balance
    }
