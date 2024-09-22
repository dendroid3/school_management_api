from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from databaseConnection import localSession
from fastapi.middleware.cors import CORSMiddleware
from datatableStructure import UserStructure, StudentStructure, GradeStructure, AttendanceStructure
from sqlalchemy.orm import Session
from pydanticModels import UserPydanticModel, StudentPydanticModel, GradePydanticModel, AttendancePydanticModel
from datetime import datetime, timedelta

app = FastAPI()

origins = [
    "http://localhost:5173",  
    "http://localhost:5174",  
    "https://lib-frontend-ehrc.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register_user(user: UserPydanticModel, db: Session = Depends(get_db)):
    created_user = UserStructure(email=user.email, id=user.id, role=user.role)
    db.add(created_user)
    db.commit()
    return "You have successfully created an account with us. Thank you!"


@app.get("/teachers/get_all")
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = db.query(UserStructure).filter(UserStructure.role == 1).all()
    return teachers

@app.delete("/teachers/delete/{user_id}")
def delete_teacher(user_id: str, db: Session = Depends(get_db)):
    teacher = db.query(UserStructure).filter(UserStructure.id == user_id).first()
    db.delete(teacher)
    db.commit()

    return "Teacher deleted successfully"

@app.get("/student/add/{teacher_id}/{registration_number}/{first_name}/{surname}/{level}")
def add_student(first_name: str, surname: str, level: str, teacher_id: str, registration_number: str, db: Session = Depends(get_db)):
    created_student = StudentStructure( first_name=first_name, surname=surname, level=level, registration_number = registration_number, teacher_id=teacher_id)
    db.add(created_student)
    db.commit()
    return "Student added successfully"

@app.get("/students/{teacher_id}/get")
def get_my_student(teacher_id: str, db: Session = Depends(get_db)):
    my_students = db.query(StudentStructure).filter(StudentStructure.teacher_id == teacher_id).all()
    return my_students

@app.delete("/student/delete/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(StudentStructure).filter(StudentStructure.id == student_id).first()
    db.delete(student)
    db.commit()
    return "Student deleted successfully."

@app.get("/student/add_grade/{student_id}/{subject}/{mark}")
def add_grade(student_id: int, subject: str, mark: int, db: Session = Depends(get_db)):
   grade_letter = calculate_grade(mark)
   now = datetime.now()
   date = now.strftime("%d-%m-%Y")

   created_grade = GradeStructure(student_id=student_id, mark=mark, grade=grade_letter, subject=subject, date=date)
   db.add(created_grade)
   db.commit()
   return "Grade Recorded Successfully" 
    

def calculate_grade(mark: int):
    if mark < 40:
        return "F"
    elif mark > 40 and mark <= 50:
        return "D"
    elif mark > 50 and mark <= 60:
        return "C"
    elif mark > 60 and mark <= 70:
        return "B"
    else:
        return "A"
    
@app.get("/student/get_one/{student_id}")
def get_one_user(student_id: int, db: Session = Depends(get_db)):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    student =  db.query(StudentStructure).filter(StudentStructure.id == student_id).first()
    student.grades = db.query(GradeStructure).filter(GradeStructure.student_id == student_id).all()
    student.attandance = db.query(AttendanceStructure).filter(AttendanceStructure.student_id == student_id).all()
    attandance_today = db.query(AttendanceStructure).filter(AttendanceStructure.student_id == student_id).filter(date == date).first()

    if attandance_today:
        student.attandance_today =  True 
    else:
        student.attandance_today =  None 
    return student

@app.get("/teacher/get_students/{teacher_id}")
def get_teachers_students(teacher_id: str, db: Session = Depends(get_db)):
    students = db.query(StudentStructure).filter(StudentStructure.teacher_id == teacher_id).all()
    for student in students:
        student.grades = db.query(GradeStructure).filter(GradeStructure.id == student.id).all()
    return students

@app.get("/student/{student_id}/mark_present")
def mark_student_present(student_id: int, db: Session = Depends(get_db)):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    attandance = db.query(AttendanceStructure).filter(AttendanceStructure.student_id == student_id).filter(date == date).first()
    if attandance:
        return "Student already marked present today"
    
    created_attendance = AttendanceStructure(student_id=student_id, date=date, total_attendances_for_class=1)
    db.add(created_attendance)
    db.commit()
    return "Student marked present"

@app.get("/teacher/{teacher_id}/get_student_attendances")
def get_student_attendances(teacher_id: str, db: Session = Depends(get_db)):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    number_attendance_today = 0
    teachers_students = db.query(StudentStructure).filter(StudentStructure.teacher_id == teacher_id).all()
    for student in teachers_students:
 
        attandance = db.query(AttendanceStructure).filter(AttendanceStructure.student_id == student.id).filter(date == date).first()
        if attandance:
            number_attendance_today += 1
    return number_attendance_today
