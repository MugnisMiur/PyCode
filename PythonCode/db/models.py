import uuid
from datetime import datetime
from enum import Enum
from sqlite3 import Binary

from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

Time1 = datetime.now()
Time = Time1.strftime('%Y-%m-%d %H:%M:%S')


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"
    ROLE_PORTAL_MANAGER = "ROLE_PORTAL_MANAGER"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(String, nullable=False)


class Article(Base):
    __tablename__ = "article"

    article_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    article_name = Column(String, nullable=False)
    engl_article_name = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    engl_authors = Column(String, nullable=False)
    author_city_first = Column(String, nullable=False)
    author_city_second = Column(String, nullable=False)
    engl_author_city_first = Column(String, nullable=False)
    engl_author_city_second = Column(String, nullable=False)
    annotation = Column(String, nullable=False)
    keywords = Column(String, nullable=False)
    engl_annotation = Column(String, nullable=False)
    engl_keywords = Column(String, nullable=False)
    introduction = Column(String, nullable=False)
    theory = Column(String, nullable=False)
    results = Column(String, nullable=False)
    conclusion = Column(String, nullable=False)
    thanks = Column(String, nullable=False)
    list_of_sources = Column(String, nullable=False)
    doc_article = Column(BYTEA, nullable=False)


class Event(Base):
    __tablename__ = "events"

    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True))
    user_id = Column(UUID(as_uuid=True))
    event_name = Column(String, nullable=False)
    application_name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(String, nullable=False, default=Time)
    status = Column(String, default='Заявка не осмотрена', nullable=False)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manager_id = Column(UUID)
    application_id = Column(UUID,  nullable=True)
    manager_name = Column(String, nullable=False)
    manager_surname = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(String, nullable=False, default=Time)


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_name = Column(String, nullable=False)
    application_id = Column(UUID)
    user_id = Column(UUID)
    status = Column(Boolean(), default=True)
    date = Column(String, nullable=False, default=Time)

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    @property
    def is_manager(self) -> bool:
        return PortalRole.ROLE_PORTAL_MANAGER in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self) -> list:
        if not self.is_admin:
            return [role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN]


