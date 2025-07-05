from database import Base
from datetime import datetime, timezone
from sqlalchemy import (
    String,
    DateTime,
    Text,
    Table,
    Column,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

note_tag_association: Table = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(length=36), ForeignKey(column="Note.id")),
    Column("tag_id", String(length=36), ForeignKey(column="Tag.id")),
)


class Note(Base):
    __tablename__ = "Note"

    id: Column[str] = Column(String(length=36), primary_key=True)
    user_id: Column[str] = Column(String(length=36), nullable=False, index=True)
    title: Column[str] = Column(String(length=64), nullable=False)
    content: Column[str] = Column(Text, nullable=False)
    memo_date: Column[str] = Column(String(length=8), nullable=False)
    created_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.now(tz=timezone.utc)
    )
    updated_at: Column[datetime] = Column(
        DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )

    tags = relationship(
        argument="Tag",
        secondary=note_tag_association,
        back_populates="notes",
    )


class Tag(Base):
    __tablename__ = "Tag"

    id: Column[str] = Column(String(length=36), primary_key=True)
    name: Column[str] = Column(String(length=64), nullable=False, unique=True)
    created_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.now(tz=timezone.utc)
    )
    updated_at: Column[datetime] = Column(
        DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )

    notes = relationship(
        argument="Note",
        secondary=note_tag_association,
        back_populates="tags",
    )
