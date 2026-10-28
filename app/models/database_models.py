from datetime import datetime, timezone
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id")
    )
    category: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(20))
    summary: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(
        nullable=True
    )
    suspicious_content: Mapped[bool] = mapped_column(
        default=False
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id")
    )
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )
    verified: Mapped[bool] = mapped_column(default=False)


class Draft(Base):
    __tablename__ = "drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id")
    )
    draft_text: Mapped[str] = mapped_column(Text)
    tone: Mapped[str] = mapped_column(String(20))
    approval_status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )