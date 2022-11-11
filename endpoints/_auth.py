import os
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from pydantic import EmailStr
from starlette import status
from schema.ResetPasswordSchema import Reset_password, confirm
from schema.TokenSchema import Token, Login
from repositories.user import UserRepository
from schema.UserSchema import UserIn, User
from ._depends import get_user_repository

router = APIRouter()


path = os.path.join("/static")


@router.post("/register-user", response_model=User)
async def register(user: UserIn, users: UserRepository = Depends(get_user_repository)):
    if await users.get_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такой Email уже существует!")
    user_avatar = os.path.join(path, 'avatars/', "not_image.png")
    if user.is_mentor:
        return await users.MentorRegister(u=user, p=user_avatar)
    else:
        return await users.UserRegister(u=user, p=user_avatar)


@router.post("/login", response_model=Token)
async def login(login: Login,
                users: UserRepository = Depends(get_user_repository)):
    return await users.login(login=login)


@router.post("/forgot-password")
async def forgot_password(email: EmailStr,
                          users: UserRepository = Depends(get_user_repository)):
    return await users.reset_password(email=email)


@router.patch("/confirm-password/")
async def confirm_password(req: confirm,
                           users: UserRepository = Depends(get_user_repository)):
    return await users.confirm_password(body=req)
