from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from core.UploaderFile import Handle_file_upload
from endpoints._depends import get_user_repository, get_current_authenticated, get_engine_of_avatar
from repositories.user import UserRepository
from schema.CourseSchema import CourseScheme
from schema.UserSchema import User

router = APIRouter()


@router.get("/read-courses", response_model=List[CourseScheme])
async def read_courses(limit: int = 100, skip: int = 0, User: UserRepository = Depends(get_user_repository)):
    return await User.get_all(limit=limit, skip=skip)


@router.post("/update-avatar", response_model=User)
async def Update_Avatar(newAvatar: UploadFile = File(),
                        current_user: User = Depends(get_current_authenticated),
                        UserRep: UserRepository = Depends(get_user_repository),
                        engineoffile: Handle_file_upload = Depends(get_engine_of_avatar)):
    types = ['image/jpeg', 'image/png']
    if newAvatar.content_type not in types:
        raise HTTPException(status_code=406, detail=f"Only {types} files allowed")
    link = await engineoffile.handle_file(newAvatar)
    return await UserRep.ChangeAva(link_of_photo=link, user=current_user)
