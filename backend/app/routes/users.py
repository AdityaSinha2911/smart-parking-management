from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = create_user(db, user_data)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return user


@router.get(
    "/",
    response_model=list[UserResponse]
)
def read_users(
    db: Session = Depends(get_db)
):

    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = update_user(db, user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete(
    "/{user_id}"
)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_user(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }