from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Optional


class Account(BaseModel):
    name: Optional[str]
    id_account: Optional[int]
    balance: int = 0
    tstamp: Optional[datetime]

    class Config:
        validate_assignment = True
        orm_mode = True


class Invoice(Account):
    operation: int

    class Config:
        orm_mode = True
