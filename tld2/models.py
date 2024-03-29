import datetime
import enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum as PgEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from tld2.db import Base


class Status(enum.Enum):
    APPROVED = 1
    MALWARE = 2
    UNTESTED = 3


class RolesEnum(enum.Enum):
    USER = 1
    APPROVER = 2
    MANAGER = 3
    ADMIN = 4


association_table = Table(
    'association_table',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('library_id', ForeignKey('libraries.id'), primary_key=True, index=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True, index=True),
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())

    approvers = relationship('Approver', back_populates='user')
    roles = relationship('Role', back_populates='user')

    def __repr__(self):
        return f'id {self.id}, {self.fullname}'


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[RolesEnum] = mapped_column(PgEnum(RolesEnum))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    registered_at: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())

    user = relationship('User', back_populates='roles')

    def __repr__(self):
        return f'Roles {id}'


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    registered_at: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())

    approvers = relationship('Approver', back_populates='company')
    managers = relationship('Manager', back_populates='company')

    def __repr__(self):
        return f'Company {self.id}, {self.name}'


class Manager(Base):
    __tablename__ = 'managers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fullname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('companies.id'), nullable=True)
    registered_at: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())

    company = relationship('Company', back_populates='managers')


class Approver(Base):
    __tablename__ = 'approvers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fullname: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    registered_at: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.date.today())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('companies.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)

    user = relationship('User', back_populates='approvers')
    company = relationship('Company', back_populates='approvers')
    approved_libraries = relationship('ApprovedLibrary', back_populates='approver')

    def __repr__(self):
        return f'Approver {self.id}, company_id {self.company_id}'


class ApprovedLibrary(Base):
    __tablename__ = 'approved_libraries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    approver_id: Mapped[int] = mapped_column(Integer, ForeignKey('approvers.id'))
    library_id: Mapped[int] = mapped_column(Integer, ForeignKey('libraries.id'))

    approver = relationship('Approver', back_populates='approved_libraries')
    library = relationship('Library', back_populates='approved_libraries')

    def __repr__(self):
        return f'Approved Library {self.id}, {self.name}'


class Library(Base):
    __tablename__ = 'libraries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    status: Mapped[Status] = mapped_column(PgEnum(Status), index=True)

    approved_libraries = relationship('ApprovedLibrary', back_populates='library')
    authors = relationship('Author', secondary=association_table, back_populates='libraries')

    def __repr__(self):
        return f'Library {self.id}, {self.name}'


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)

    libraries = relationship('Library', secondary=association_table, back_populates='authors')

    def __repr__(self):
        return f'Author {self.id}, {self.name}'
