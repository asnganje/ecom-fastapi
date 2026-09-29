from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user, get_db
from app.modules.address.schema import AddressRead, AddressCreate, AddressUpdate
from app.modules.address.service import AddressService
from app.modules.users.model import User

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AddressRead])
def list_my_addresses(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    a_service = AddressService(db)
    return a_service.list_my_addresses(current_user)

@router.get("/{address_id}", status_code=status.HTTP_200_OK, response_model=AddressRead)
def get_address(address_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    a_service = AddressService(db)
    return a_service.get_address(current_user, address_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AddressRead)
def create_address(payload: AddressCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    a_service = AddressService(db)
    return a_service.create_address(payload, current_user)
@router.patch("/{address_id}", status_code=status.HTTP_200_OK, response_model=AddressRead)
def update_address(address_id:int, payload: AddressUpdate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    a_service = AddressService(db)
    return a_service.update_address(address_id, payload, current_user)

@router.delete("/{address_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_address(address_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    a_service = AddressService(db)
    a_service.delete_address(current_user, address_id)
    return {"msg":"address deleted successfully!"}


