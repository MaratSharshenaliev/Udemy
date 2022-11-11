import datetime

import pytz
import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.config import HOSTNAME_AND_PORT
from db.models.Course import Course
from db.models.User import users
from db.models.Reset_Password_time_db import Reset_password_cache
from schema.ResetPasswordSchema import Reset_password, confirm, TemplateCorfirmSzhema
from schema.StaticSchema import Static
from schema.TokenSchema import Login, Token
from schema.UserSchema import User, UserIn
from core.security import hash_password, verify_password, create_access_token
from .base import BaseRepository
from fastapi import HTTPException, status


class UserRepository(BaseRepository):
    async def MentorRegister(self, u: UserIn, p: str) -> JSONResponse:
        user = User(
            firstname=u.firstname,
            lastname=u.lastname,
            audience=u.audience,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            avatar=p,
            type=p[-3:],
            is_mentor=u.is_mentor
        )
        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        await self.database.execute(query)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))

    async def UserRegister(self, u: UserIn, p: str) -> JSONResponse:
        user = User(
            firstname=u.firstname,
            lastname=u.lastname,
            audience=u.audience,
            email=u.email,
            hashed_password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            avatar=p,
            type=p[-3:]
        )
        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        await self.database.execute(query)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))

    async def login(self, login: Login) -> JSONResponse:
        user = await self.get_by_email(login.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не существует")
        if not verify_password(login.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный пороль")

        response = JSONResponse(status_code=status.HTTP_201_CREATED, content=Token(
            access_token=create_access_token({"sub": user.email}),
            token_type="Bearer"
        ).dict())
        return response

    async def reset_password(self, email: str) -> JSONResponse:
        user = await self.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не существует")
        reset_code = str(uuid.uuid1())

        reset_ready = Reset_password(email=email, reset_code=reset_code, status="1",
                                     reset_code_created_at=datetime.datetime.utcnow())
        values = {**reset_ready.dict()}
        values.pop("id", None)
        query2 = Reset_password_cache.insert().values(**values)
        reset_ready.id = await self.database.execute(query2)
        __link = HOSTNAME_AND_PORT[0] + ":" + HOSTNAME_AND_PORT[1] + f"/reset-password/?token={reset_code}"
        subject = "Hello from Udemy"
        recipients = [reset_ready.email]
        subtype = "html"
        data = TemplateCorfirmSzhema(firstname=user.firstname, url_confirm=__link)

        # from core.EmailUtils import send_to_email
        # return await send_to_email(subject=subject, recipients=recipients, data=data, subtype=subtype)
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"detail": "while service isn`t "
                                                                                                "working"})

    async def confirm_password(self, body: confirm) -> JSONResponse:
        Exceptions = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Время на cсылку восстановление истек! Повторите попытку")
        # Через 24 часа после отправки письма, ссылка для восстановления пароля становится неактивной.
        timeleft: datetime = datetime.datetime.now(tz=pytz.timezone("UTC")) - datetime.timedelta(hours=24)

        # Запрос дынных сохраненных запросов кода восстановление
        query = Reset_password_cache.select().where(Reset_password_cache.c.status == '1',
                                                    Reset_password_cache.c.reset_code == body.token)
        reset_token = await self.database.fetch_one(query)

        # Валидация на срок годность ссылки восстановление
        if not reset_token:
            raise Exceptions
        elif str(timeleft) > str(reset_token["reset_code_created_at"]):
            raise Exceptions

        # Запрос дынных пользователя после валидации получить email  и обновить пароль
        u = await self.get_by_email(reset_token["email"])
        user = User(
            firstname=u.firstname,
            lastname=u.lastname,
            email=u.email,
            is_mentor=u.is_mentor,
            hashed_password=hash_password(body.password),
            created_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop("id", None)
        values.pop("created_at", None)
        query = users.update().where(users.c.email == u.email).values(**values)
        await self.database.execute(query=query)

        # Удаляем запрошенные ссылки дынне из базы данных

        query = Reset_password_cache.delete().where(Reset_password_cache.c.email == user.email)
        await self.database.execute(query=query)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=user)

    async def get_by_email(self, email: str) -> User or None:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_all(self, limit: int = 100, skip: int = 0) -> JSONResponse:
        query = Course.select().limit(limit).offset(skip).where(Course.c.CourseActivated != True)
        parsed = await self.database.fetch_all(query=query)
        parsed = list(jsonable_encoder(parsed))
        if not parsed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пока курсов нету")
        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed)

    async def ChangeAva(self, link_of_photo: str, user: User):
        user.avatar = link_of_photo
        user.type = link_of_photo[-3:]
        values = {**user.dict()}
        values.pop("id", None)
        UserId = int(user.id)
        query = users.update().where(users.c.id == UserId).values(**values)
        await self.database.execute(query=query)
        parsed = jsonable_encoder(values)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=parsed)
