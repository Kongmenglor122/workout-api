from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

DUMMY_PASSWORD_HASH = hash_password("dummy-password-for-timing")


@router.post(
    "/register",
    status_code=201,
    response_model=schemas.UserResponse,
)
def register_user(
    body: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    email = str(body.email).lower()

    statement = select(models.User).where(
        models.User.email == email
    )
    existing_user = db.scalars(statement).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = models.User(
        email=email,
        password_hash=hash_password(body.password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        existing_user = db.scalars(statement).first()

        if existing_user is not None:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered",
            )

        raise

    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
)
def login_user(
    body: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    email = str(body.email).lower()

    statement = select(models.User).where(
        models.User.email == email
    )
    user = db.scalars(statement).first()

    stored_hash = (
        user.password_hash
        if user is not None
        else DUMMY_PASSWORD_HASH
    )
    password_matches = verify_password(
        body.password,
        stored_hash,
    )

    if user is None or not password_matches:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return schemas.TokenResponse(
        access_token=create_access_token(user.id),
    )