from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import (
    create_connection,
    create_student,
    get_students,
    get_student_by_id,
    update_student,
    delete_student,
)

app = FastAPI()
client = create_connection()


class Student(BaseModel):
    name: str
    age: int
    grade: str


@app.post("/students/")
def api_create_student(student: Student):
    create_student(client, student.model_dump())
    return {"message": "Student created successfully"}


@app.get("/students/")
def api_get_students():
    students = get_students(client)
    return students


@app.get("/students/{student_id}")
def api_get_student(student_id: str):
    student = get_student_by_id(client, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}")
def api_update_student(student_id: str, student: Student):
    update_student(client, student_id, student.model_dump())
    return {"message": "Student updated successfully"}


@app.delete("/students/{student_id}")
def api_delete_student(student_id: str):
    delete_student(client, student_id)
    return {"message": "Student deleted successfully"}
