from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.modules.address.model import Address
from app.modules.address.repository import AddressRepository
from app.modules.address.schema import AddressRead, AddressCreate, AddressUpdate
from app.modules.users.model import User


class AddressService():
    def __init__(self, db:Session)->None:
        self.repository = AddressRepository(db)
    def _dump_address(self,address:Address) -> AddressRead:
        return AddressRead.model_validate(address)
    def list_my_addresses(self, current_user:User)->list[AddressRead]:
        user_id=current_user.id
        addresses = self.repository.get_address_by_user_id(user_id)
        return [self._dump_address(address) for address in addresses]
    def get_address(self, current_user:User, address_id:int)->AddressRead:
        address = self.repository.get_address_by_id(address_id)
        user_id = current_user.id
        if address is None or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not accessed"
            )
        return self._dump_address(address)

    def create_address(self, payload:AddressCreate, current_user:User)->AddressRead:
        user_id = current_user.id
        if payload.is_default:
            self.repository.unset_default_for_user(user_id)
        address = Address(
            user_id=user_id,
            **payload.model_dump()
        )

        db_address = self.repository.create_address(address)
        return self._dump_address(db_address)

    def update_address(self, address_id:int, payload: AddressUpdate, current_user:User)->AddressRead:
        address = self.repository.get_address_by_id(address_id)
        user_id = current_user.id
        if address is None or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        changes=payload.model_dump(exclude_unset=True, exclude_none=True)

        if changes.get("is_default") is True:
            self.repository.unset_default_for_user(user_id)
        for field, value in changes.items():
            setattr(address, field, value)

        db_address = self.repository.update(address)
        return self._dump_address(db_address)

    def delete_address(self, current_user:User, address_id:int)->None:
        address = self.repository.get_address_by_id(address_id)
        user_id = current_user.id
        if address is None or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        self.repository.delete(address)






