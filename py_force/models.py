from pydantic import BaseModel
from typing import Optional


class Account(BaseModel):
    """
    A schema class for Salesforce Accounts
    """
    Name: Optional[str] = ''
    NumberOfEmployees: Optional[int] = 0
    ShippingState: Optional[str] = ''
    ShippingPostalCode: Optional[str] = ''
    ShippingCity: Optional[str] = ''
    ShippingStreet: Optional[str] = ''
