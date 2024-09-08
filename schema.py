from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    login_type: str
    password: str

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)
    email: str | None = None
    phone_number: str | None = None
    gander: str = Field(min_length=3, max_length=6)

class AdminCreateUserSchema(BaseModel):
    username: str
    password: str
    role: str
    gander: str

class AddBookSchema(BaseModel):
    title: str
    description: str
