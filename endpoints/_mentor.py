import os
from typing import List

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException

from core.UploaderFile import Handle_file_upload
from endpoints._depends import get_current_Mentor, get_mentor_repository, get_engine_of_avatar, \
    get_engine_of_CourseFiles
from schema import CourseSchema
from schema.CourseSchema import CourseInScheme, CourseScheme, CourseItemSchemaIn, CourseUpdateSchema, CourseItemSchema
from schema.UserSchema import User
from ._depends import MentorRepository

router = APIRouter()
path = os.path.join("/static")


@router.post("/create-course", response_model=CourseScheme)
async def Create_Course(course: CourseInScheme,
                        current_mentor: User = Depends(get_current_Mentor),
                        CourseRepo: MentorRepository = Depends(get_mentor_repository)):
    not_imageorvideo = os.path.join(path, 'avatars/', "not_image.png")
    return await CourseRepo.createCourse(user_id=current_mentor.id, c=course, Urls=not_imageorvideo)


@router.post("/create-course-file", response_model=CourseScheme)
async def upload_files_Course(
                        idCourse: int,
                        video: UploadFile = File(),
                        picture: UploadFile = File(),
                        current_mentor: User = Depends(get_current_Mentor),
                        CourseRepo: MentorRepository = Depends(get_mentor_repository),
                        engineoffile: Handle_file_upload = Depends(get_engine_of_CourseFiles)):
        types = ['video/mp4', 'image/jpeg', 'image/png']
        if video.content_type != types[0]:
            raise HTTPException(status_code=406, detail=f"For video files allowed mp4 types")
        elif picture.content_type not in types[0:]:
            raise HTTPException(status_code=406, detail=f"For picture files allowed {types[0:]} types")
        Urls = await engineoffile.handle_many_files_saver([video, picture])
        course = await CourseRepo.get_course_by_id(idCourse=idCourse, user_id=current_mentor.id)
        course = CourseScheme.parse_obj(course)
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course has not found")

        print(course)
        course.image = Urls.get("image")
        course.video = Urls.get("video")

        return await CourseRepo.update(idCourse=idCourse, user_id=current_mentor.id, j=course)


@router.post("/create-course-item", response_model=CourseItemSchema)
async def Create_Course_Item(
        idCourse: int,
        data: CourseItemSchemaIn,
        current_mentor: User = Depends(get_current_Mentor),
        Mentor: MentorRepository = Depends(get_mentor_repository)):
    return await Mentor.create_CourseItem(idCourse=idCourse, data=data)


@router.post("/create-course-item-file", response_model=CourseItemSchema)
async def Create_Course_Item_file(
        idCourseItem: int,
        idCourse: int,
        file: UploadFile = File(),
        current_mentor: User = Depends(get_current_Mentor),
        Mentor: MentorRepository = Depends(get_mentor_repository),
        engineoffile: Handle_file_upload = Depends(get_engine_of_CourseFiles)):
    types = ["application/pdf", "application/csv", "text/csv"]
    if file.content_type not in types:
        raise HTTPException(status_code=406, detail=f"Only {types} files allowed")
    link = await engineoffile.handle_file(file)
    return await Mentor.upload_file_to_Course_Item(filename=link, idCourseItem=idCourseItem, CourseId=idCourse)


@router.get("/get-course-to-update", response_model=CourseUpdateSchema)
async def Get_Course_To_Update(idCourse: int,
                        current_mentor: User = Depends(get_current_Mentor),
                        Mentor: MentorRepository = Depends(get_mentor_repository)):
    response = await Mentor.get_course_by_id(idCourse=idCourse, user_id=current_mentor.id)
    return CourseUpdateSchema.parse_obj(response)


@router.post("/update-course", response_model=CourseScheme)
async def update_Course(idCourse: int,
                        new_course: CourseInScheme,
                        current_mentor: User = Depends(get_current_Mentor),
                        Mentor: MentorRepository = Depends(get_mentor_repository)):
    return await Mentor.update(idCourse=idCourse, user_id=current_mentor.id, j=new_course)


@router.get("/deactive-courses", response_model=List[CourseScheme])
async def get_Deactive_Course(
                        current_mentor: User = Depends(get_current_Mentor),
                        Mentor: MentorRepository = Depends(get_mentor_repository)):
    return await Mentor.deactiveCoure(UserId=current_mentor.id)


@router.get("/get-courses", response_model=List[CourseScheme])
async def get_courses(
        current_mentor: User = Depends(get_current_Mentor),
        Mentor: MentorRepository = Depends(get_mentor_repository)):
    return await Mentor.get_all_course(current_mentor.id)


# @router.delete("/delete-course")
# async def delete_Course(idCourse: int,
#                         current_mentor: User = Depends(get_current_Mentor),
#                         Mentor: MentorRepository = Depends(get_mentor_repository)):
#     return await Mentor.delete_course(idCourse, current_mentor.id)




