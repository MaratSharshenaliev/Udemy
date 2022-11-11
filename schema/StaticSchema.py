from pydantic import BaseModel


class Static(BaseModel):
    url_name: str
    type: str
    static_user: str | int = None
    static_course: str | int = None
    static_course_content: str | int = None
    static_lecture: str | int = None