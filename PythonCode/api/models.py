import re
import uuid
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, EmailStr, validator, constr
from sqlalchemy.dialects.postgresql import BYTEA

LETTER_MATCH_PATTERN = re.compile(r"^[a-яA-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    age: int
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    age: int
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class EventCreate (BaseModel):
    name: str
    content: str
    date: str


class ArticleCreate(BaseModel):
    user_id: str
    article_name: str
    engl_article_name: str
    authors: str
    engl_authors: str
    author_city_first: str
    author_city_second: str
    engl_author_city_first: str
    engl_author_city_second: str
    annotation: str
    keywords: str
    engl_annotation: str
    engl_keywords: str
    introduction: str
    theory: str
    results: str
    conclusion: str
    thanks: str
    list_of_sources: str


class ApplicationCreate(BaseModel):
    event_id: str
    user_id: str
    event_name: str
    application_name: str
    content: str


class CommentCreate(BaseModel):
    application_id: str
    manager_id: str
    manager_name: str
    manager_surname: str
    content: str


class NotificationCreate(BaseModel):
    application_id: str
    application_name: str
    user_id: str


class ShowNotification(TunedModel):
    application_id: uuid.UUID
    application_name: str
    user_id: str
    status: bool
    date: datetime


class ShowEvent (TunedModel):
    event_id: uuid.UUID
    name: str
    content: str
    is_active: bool
    date: str


class ShowArticle(TunedModel):
    article_name: str
    engl_article_name: str
    authors: str
    engl_authors: str
    author_city_first: str
    author_city_second: str
    engl_author_city_first: str
    engl_author_city_second: str
    annotation: str
    keywords: str
    engl_annotation: str
    engl_keywords: str
    introduction: str
    theory: str
    results: str
    conclusion: str
    thanks: str
    list_of_sources: str


class ShowApplication (TunedModel):
    id: uuid.UUID
    event_id: str
    user_id: str
    event_name: str
    application_name: str
    content: str
    date: datetime
    status: str


class ShowComment (TunedModel):
    id: uuid.UUID
    application_id: str
    manager_id: str
    manager_name: str
    manager_surname: str
    content: str
    date: datetime


# class ApplicationBase (SQLModel):
#     id: uuid.UUID = Field(index=True)
#     event_id: uuid.UUID = Field(index=True)
#     user_id: uuid.UUID = Field(index=True)
#     content: str
#     date: str
#     status: str
#
#
# class CommentBase (SQLModel):
#     id: uuid.UUID = Field(index=True)
#     manager_id: uuid.UUID = Field(index=True)
#     application_id: Optional[uuid.UUID] = Field(foreign_key="application.id")
#     content: str
#     date: str
#
#
# class Application(ApplicationBase, table=True):
#     id: Optional[uuid.UUID] = Field(primary_key=True)
#
#     heroes: List["Comment"] = Relationship(back_populates="application")
#
#
# class Comment(CommentBase, table=True):
#     id: Optional[uuid.UUID] = Field(primary_key=True)
#
#     team: Optional[Application] = Relationship(back_populates="comment")
#
#
# class ApplicationRead (ApplicationBase):
#     id: uuid.UUID
#
#
# class CommentsRead (CommentBase):
#     id: uuid.UUID
#
#
# class ApplicationWithComments(ApplicationRead):
#     comments: List[CommentsRead] = []


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class DeleteEventResponse(BaseModel):
    deleted_event_id: uuid.UUID


class UpdateUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserNameRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr


class UpdatedUserName(BaseModel):
    name: str
    surname: str
    email: EmailStr
    user_id: uuid.UUID


class UpdateEventRequest(BaseModel):
    name: str
    content: str


class UpdateStatusApplication(BaseModel):
    status: str


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class Token(BaseModel):
    name: str
    surname: str
    roles: str
    user_id: uuid.UUID
    access_token: str
    token_type: str
