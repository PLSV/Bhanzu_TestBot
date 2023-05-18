from pydantic import BaseModel


class UserData(BaseModel):
    name: str
    grade: str
    teacher: str


class capture_response_model(BaseModel):
    option_chosen: str
    question_number: str
    reason: str