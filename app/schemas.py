from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    UUID: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    UUID: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(UserBaseSchema):
    id: str


class CandidateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    UUID: int
    career_level: str # ex: Junior, Senior, Mid Level…
    job_major: str # ex: Computer Science, Computer Information Systems,...
    years_of_experience: int
    degree_type: str #ex: Bachelor, Master, High School,...
    skills: str
    nationality: str
    city: str
    salary: float
    gender: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True