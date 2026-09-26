from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    full_name:str = Field(min_length=3, max_length=100, description="Fullname of the user")
    email:EmailStr = Field(description="Email of the user")
    password:str = Field(min_length=8, max_length=255, description="Password of the user")

class LoginRequest(BaseModel):
    email:EmailStr = Field(description="Email of the user")
    password:str =Field(min_length=8, max_length=255, description="Password of the user")