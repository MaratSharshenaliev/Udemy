# from typing import List
#
# from fastapi import APIRouter, Depends, status
# from starlette.responses import JSONResponse
# from fastapi.requests import Request
# from endpoints._depends import get_course_repository, get_current_Superuser
# from schema.CourseSchema import CourseInScheme, CourseScheme
# from schema.UserSchema import User
# from ._depends import MentorRepository
#
# router = APIRouter()
#
#
# @router.post("/get-deactive-courses", response_model=List[CourseScheme])
# async def get_Course(current_superuser: User = Depends(get_current_Superuser),
#                      CourseRepo: MentorRepository = Depends(get_course_repository)):
#     return await CourseRepo.getDeactivatedCourse()