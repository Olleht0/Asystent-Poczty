from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.database_models import Email
from app.models.schemas import EmailCreate, EmailRead

router = APIRouter(prefix="/emails", tags=["Emails"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[EmailRead])
def get_emails(db: DbSession):
    statement = select(Email).order_by(Email.id.desc())
    return db.scalars(statement).all()


@router.get("/{email_id}", response_model=EmailRead)
def get_email(email_id: int, db: DbSession):
    email = db.get(Email, email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Wiadomość nie istnieje"
        )

    return email


@router.post(
    "",
    response_model=EmailRead,
    status_code=201,
)
def create_email(email_data: EmailCreate, db: DbSession):
    email = Email(**email_data.model_dump())

    db.add(email)
    db.commit()
    db.refresh(email)

    return email