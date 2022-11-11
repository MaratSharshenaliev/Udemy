from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse

from db.models.Course import *
from schema import CourseSchema
from .base import BaseRepository
from schema.CourseSchema import CourseInScheme, CourseScheme, CourseItemSchemaIn, CourseItemSchema, \
    CourseItemFileSchema


class MentorRepository(BaseRepository):

    async def createCourse(self, user_id, c: CourseInScheme, Urls: str) -> JSONResponse:
        course = CourseScheme(Category=c.Category,
                              SubCategory=c.SubCategory,
                              Tittle=c.Tittle,
                              subTittle=c.subTittle,
                              Description=c.Description,
                              language=c.language,
                              level=c.level,
                              cost=c.cost,
                              currency=c.currency,
                              CourseActivated=False,
                              CourseContentIsNull=True,
                              user_id=user_id,
                              video=Urls,
                              image=Urls
                              )
        values = {**course.dict()}
        values.pop("id", None)
        query = Course.insert().values(**values)
        id = await self.database.execute(query)
        values["id"] = id
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=values)

    async def update(self, idCourse: int, user_id: int, j) -> JSONResponse:
        to_update = await self.get_course_by_id(idCourse, user_id)
        to_update = CourseScheme.parse_obj(to_update)
        values = {**to_update.dict()}
        values.update(j)
        values.pop("id", None)
        query = Course.update().where(Course.c.id == idCourse, Course.c.user_id == user_id).values(**values)
        await self.database.execute(query=query)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=values)

    async def deactiveCoure(self, UserId: int) -> JSONResponse:
        query = Course.select().where(Course.c.user_id == UserId, Course.c.CourseActivated == False)
        value = await self.database.fetch_all(query=query)
        if value is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пока неактивных курсов нету!")
        pased = list(jsonable_encoder(value))
        return JSONResponse(status_code=status.HTTP_200_OK, content=pased)

    async def get_all_course(self, UserId:int):
        query = Course.select().where(Course.c.user_id == UserId)
        value = await self.database.fetch_all(query=query)
        if value is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пока ваших курсов нету!")
        pased = list(jsonable_encoder(value))
        return JSONResponse(status_code=status.HTTP_200_OK, content=pased)

    # async def delete_course(self, idCourse, UserId):
    #     req = await self.get_course_by_id(idCourse, UserId)
    #     if req is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого курса нету")
    #
    #     query = CourseItemFile.delete().where(CourseItemFile.c.CourseId == idCourse, CourseItemFile.c.CourseItemId = )
    #     await self.database.fetch_one(query=query)
    #
    #     query = CourseItem.delete().where(CourseItem.c.CourseId == idCourse)
    #     await self.database.fetch_one(query=query)
    #
    #     query = Course.delete().where(Course.c.user_id == UserId, Course.c.id == idCourse)
    #     await self.database.fetch_one(query=query)
    #
    #     # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyc2hlbmFsaWV2LjIwMDNAZ21haWwuY29tIiwiZXhwIjoxNjY4MTExMTI0fQ.Ypse3UDR4oo9XjKHVnFuGRdDgWZex7aZyynC9Cxu48c
    #     return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Deleted"})

    async def get_course_by_id(self, idCourse, user_id: int):
            query = Course.select().where(Course.c.id == idCourse, Course.c.user_id == user_id)
            value = await self.database.fetch_one(query=query)
            if value is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
            return value

    async def create_CourseItem(self, idCourse: int, data):
        SubCourse = CourseItemSchema(Tittle=data.Tittle, Description=data.Description, CourseId=idCourse)
        values = {**SubCourse.dict()}
        query = CourseItem.insert().values(**values)
        _ = await self.database.execute(query)
        values["id"] = _
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={**values})

    async def upload_file_to_Course_Item(self, filename: str, idCourseItem, CourseId):
        file = CourseItemFileSchema(file=filename, CourseItemId=idCourseItem, CourseId=CourseId)
        values = {**file.dict()}
        query = CourseItemFile.insert().values(**values)
        _ = await self.database.execute(query)
        values["id"] = _
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={**values})
