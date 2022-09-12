import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models import accounting
from database.db import get_session
from database import db_models

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/top_10_accounts",
            response_model=List[accounting.Account])
async def show_random_accounts(db: Session = Depends(get_session)):
    """
    Бстрая проверка, что таблица создалась и в ней что-то есть
    :param db:
    :return:
    """
    random_accounts = db.query(db_models.Account).limit(10).all()
    if random_accounts:
        return random_accounts
    else:
        raise HTTPException(204, "No Content")


@router.get("/check_balance/",
            response_model=List[accounting.Account])
async def show_account(id_account: int = None,
                       db: Session = Depends(get_session)):
    """
    Проверка баланса по id_account.
    :param db:
    :param id_account:
    :return:
    """
    found_account = db.query(db_models.Account).\
        filter(db_models.Account.id_account == id_account).all()
    if found_account:
        return found_account
    else:
        raise HTTPException(204, "No Content")


def create_account(account_body: accounting.Account, session: Session) -> int:
    """
    Создаем вручную клиента в t_accounts
    :param account_body:
    :param db:
    :return:
    """
    try:
        account_body.tstamp = datetime.utcnow()
        new_account = db_models.Account(**account_body.dict())
        session.add(new_account)
        session.flush()
        session.commit()
        session.refresh(new_account)
        return new_account
    except Exception as e:
        logging.error(f'Create_account: {e}')


@router.post("/create_account",
             response_model=dict)
async def add_account(body: accounting.Account, db: Session = Depends(get_session)):
    """
    Создать аккаунт, если вдруг захотелось сделать это вручную
    :param body:
    :param db:
    :return:
    """
    body.tstamp = datetime.utcnow()
    new_account = db_models.Account(**body.dict())
    db.add(new_account)
    db.flush()
    db.commit()
    db.refresh(new_account)
    if new_account.id_account:
        return {'inserted_id': new_account.id_account}
    else:
        raise HTTPException(500, "Account insert error")


@router.post("/update_balance",
             response_model=dict)
async def update_balance(invoice: accounting.Invoice, db: Session = Depends(get_session)):
    """
    Метод получает инвойс. Создает клиента, если такого его не было.
    Если такой клиент был в БД, то считает ему баланс и обновляет в БД.
    :param invoice:
    :param db:
    :return:
    """
    t_accounts = db.query(db_models.Account)
    accounts = t_accounts.filter_by(id_account=invoice.id_account).\
        order_by(db_models.Account.id_account).all()
    count_accounts_by_id = len(accounts)
    account = accounting.Account(**invoice.dict(exclude={'operation', 'id'}))
    account.tstamp = datetime.utcnow()
    if count_accounts_by_id > 1:
        # Такой ситуации не должно происходить, если id_account primary_key в БД
        logging.warning(f'More 1 account in t_accounts by id_account {invoice.id_account}')
    upd_account = db_models.Account(**account.dict())
    if count_accounts_by_id == 0:
        logging.info(f'Create new account with id_account {invoice.id_account}')
        upd_account.balance = invoice.operation
        db.add(upd_account)
    else:
        old_account = accounts[0]
        upd_account.id_account = old_account.id_account
        upd_account.balance = invoice.operation + old_account.balance
        db.merge(upd_account)
    db.flush()
    db.commit()
    if account.id_account:
        return {'updated_account_id': account.id_account}
    else:
        raise HTTPException(500, "Account update error")
