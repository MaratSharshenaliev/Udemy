from fastapi import Depends, HTTPException, status
from repositories.mentor import MentorRepository
from repositories.user import UserRepository
from db.base import database
from core.security import JWTBearer, decode_access_token
from schema.UserSchema import User
from core.UploaderFile import Handle_file_upload

cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Учетные данные недействительны")


def get_mentor_repository() -> MentorRepository:
    return MentorRepository(database)


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_engine_of_avatar() -> Handle_file_upload:
    return Handle_file_upload("avatar")


def get_engine_of_CourseFiles() -> Handle_file_upload:
    return Handle_file_upload("CourseDirectory")


def get_engine_of_CourseItemFiles() -> Handle_file_upload:
    return Handle_file_upload("CourseItemFiles")


async def get_current_Superuser(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> HTTPException | User:
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        return cred_exception
    return user


async def get_current_Mentor(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> HTTPException | User:
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    if not user.is_mentor:
        raise cred_exception
    return user


async def get_current_authenticated(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> HTTPException | User:
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user
