from datetime import datetime
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import func, text

# обязательно поменять!! Пока надо протестить, что работает
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'fast_api'
DB_USER = 'admin'
DB_PASSWORD = 'Pizda123$'
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

#таблица пользователей
class User(Base):
    id: Mapped[int_pk]
    nickname: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __str__(self):
        return (f"{self.__class__.name}(id={self.id}, "
                f"nickname = {self.nickname},"
                f"email = {self.email})")

    def __repr__(self):
        return str(self)
