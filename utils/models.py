from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    grade: str
    teacher: str