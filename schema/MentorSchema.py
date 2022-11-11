
from pydantic import BaseModel


class MentorSettings(BaseModel):
    _id: any = None
    NameOfMentor: str = None
    Email: str = None
    isMentor: bool = None