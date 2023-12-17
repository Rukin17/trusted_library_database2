from pydantic import BaseModel
from tld2.models import Status, RolesEnum

class User(BaseModel):
    id: int
    username: str
    fullname: str
    email: str
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True

class Library(BaseModel):
    id: int
    name: str
    status: Status

    class Config:
        from_attributes = True


class Company(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Approver(BaseModel):
    id: int
    fullname: str
    email: str
    user_id: int
    company_id: int | None
    is_active: bool

    class Config:
        from_attributes = True


class ApprovedLibrary(BaseModel):
    id: int
    name: str
    approver_id: int
    library_id: int

    class Config:
        from_attributes = True


class Role(BaseModel):
    id: int
    user_id: int
    user_role: RolesEnum
    approver_role: RolesEnum | None
    manager_role: RolesEnum | None
    admin_role: RolesEnum | None

    class Config:
        from_attributes = True