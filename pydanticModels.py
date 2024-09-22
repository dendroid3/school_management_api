from pydantic import BaseModel

class UserPydanticModel(BaseModel):
    id: str
    email: str
    role: int

class StudentPydanticModel(BaseModel):
    id: str 
    registration_number: str
    first_name: str 
    surname: str 
    level: str 
    teacher_id: str 

class GradePydanticModel(BaseModel):
    id: int
    student_id: int
    mark: int
    grade: str
    subject: str
    date: str

class AttendancePydanticModel(BaseModel):
    id: int
    student_id: int
    date: str
    total_attendances_for_class: str
