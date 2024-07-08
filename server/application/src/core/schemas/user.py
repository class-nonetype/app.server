import pydantic
import uuid
from pydantic import BaseModel
from typing import Optional

class UserSession(BaseModel):
    client: str
    user_full_name: str
    user_id: int
    user_role_name: str
    access_token: str
    views_control_access: list[str]

class UserRole(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: uuid.UUID


class UserProfile(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    full_name: str
    e_mail: str


class UserAccount(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    username: str
    password: str


class User(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    Account: UserAccount
    Profile: UserProfile
    Role: UserRole


class CreateUser(User):
    pass

class ModifyUser(pydantic.BaseModel):
    id: uuid.UUID

class DeleteUser(pydantic.BaseModel):
    id: uuid.UUID