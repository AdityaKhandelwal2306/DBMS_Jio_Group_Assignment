from bson import ObjectId
from pymongo import MongoClient


uri = "mongodb+srv://yashjoglekar:yashjoglekar@cluster0.tisxrcq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


def create_connection():
    client = MongoClient(uri)
    return client


def create_student(client: MongoClient, data: dict):
    db = client.school
    db.students.insert_one(data)


def get_students(client: MongoClient):
    db = client.school
    return list(db.students.find(projection={"_id": False}))


def get_student_by_id(client: MongoClient, student_id: str):
    db = client.school
    return db.students.find_one(
        {"_id": ObjectId(student_id)}, projection={"_id": False}
    )


def update_student(client: MongoClient, student_id: str, data: dict):
    db = client.school
    db.students.update_one({"_id": ObjectId(student_id)}, {"$set": data})


def delete_student(client: MongoClient, student_id: str):
    db = client.school
    db.students.delete_one({"_id": ObjectId(student_id)})


if __name__ == "__main__":
    conn = create_connection()
    print(conn)
