from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.address.model import Address


class AddressRepository():
    def __init__(self, db: Session)->None:
        self.db = db
    def get_address_by_id(self, address_id:int) -> Address | None:
        return self.db.get(Address, address_id)
    def get_address_by_user_id(self, user_id:int)->list[Address]:
        statement=select(Address).where(Address.user_id == user_id).order_by(Address.id)
        return self.db.scalars(statement).all()

    def create_address(self, address:Address)->Address:
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address
    def update(self, address: Address)->Address:
        self.db.commit()
        self.db.refresh(address)
        return address
    def delete(self, address:Address)->None:
        self.db.delete(address)
        self.db.commit()

    def unset_default_for_user(self, user_id: int) -> None:
        addresses = self.get_address_by_user_id(user_id)

        for address in addresses:
            address.is_default = False
