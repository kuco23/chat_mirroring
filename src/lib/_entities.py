from enum import IntEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase

class Gender(IntEnum):
    FEMALE = 0
    MALE = 1

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True) # not obtainable with instagrapi
    gender: Mapped[bool] = mapped_column(nullable=True)
    match_id: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=True)
    # relationships
    match: Mapped["User"] = relationship("User", remote_side=[id], uselist=False)

    def __init__(self, id: str, **kwargs):
        super().__init__(id=id, **kwargs)

class Message(Base):
    __tablename__ = "message"

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    timestamp: Mapped[float] = mapped_column()
    from_user_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    to_user_id: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=True) # if it's null then it was not sent

    # to_user_id is not required at object construction, only when the object is stored to the database
    def __init__(self, id: str, from_user_id: str, content: str, timestamp: float, **kwargs):
        super().__init__(id=id, from_user_id=from_user_id, content=content, timestamp=timestamp, **kwargs)

class ProcessedMessage(Base):
    __tablename__ = "processed_message"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_message_id: Mapped[str] = mapped_column(ForeignKey('message.id'))
    content: Mapped[str] = mapped_column()

    def __init__(self, original_message_id: str, content: str, **kwargs):
        super().__init__(original_message_id=original_message_id, content=content, **kwargs)