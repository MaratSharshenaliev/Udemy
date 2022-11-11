from fastapi.encoders import jsonable_encoder
from starlette import status
from fastapi.responses import JSONResponse

from db.models.Course import *
from .base import BaseRepository


class MentorRepository(BaseRepository):

    async def getDeactivatedCourse(self) -> JSONResponse:
        query = Course.select().where(Course.c.CourseActivated == False)
        courses = await self.database.fetch_all(query)
        parsed = jsonable_encoder(courses)
        print(parsed)
        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed)

    async def getActivatedCourseBy(self) -> JSONResponse:
        query = Course.select().where(Course.c.CourseActivated == False)
        courses = await self.database.fetch_all(query)
        parsed = jsonable_encoder(courses)
        print(parsed)
        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed)
