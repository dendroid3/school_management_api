from sqlalchemy import Column, Integer, String, ForeignKey
from databaseConnection import Base, engine

class UserStructure(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    #1 == teacher, 2 == principal
    role = Column(Integer)


class StudentStructure(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    registration_number = Column(String, unique=True, index=True)
    first_name = Column(String)
    surname = Column(String)
    level = Column(String)
    teacher_id = Column(String, ForeignKey("users.id"))


class GradeStructure(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    mark = Column(Integer)
    grade = Column(String)
    subject = Column(String)
    date = Column(String)


class AttendanceStructure(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(String)
    total_attendances_for_class = Column(Integer)

Base.metadata.create_all(bind=engine)
