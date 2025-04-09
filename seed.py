import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from database.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group

fake = Faker("en_US")
Faker.seed(42)


def seed_database():
    session: Session = SessionLocal()
    try:
        groups = create_group(session)
        teachers = create_teacher(session)
        subjects = create_subject(session, teachers)
        students = create_student(session, groups)
        create_grades(session, students, subjects)
        session.commit()

        print("Database seeded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def create_group(session: Session):
    group_names = ["1-CS", "1-CS", "3-CS"]
    groups = []
    for name in group_names:
        existing_group = session.query(Group).filter_by(name=name).first()
        if not existing_group:
            group = Group(name=name)
            session.add(group)
            groups.append(group)
    session.flush()
    return groups


def create_teacher(session: Session):
    teachers = []
    for _ in range(5):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number()
        )
        session.add(teacher)
        teachers.append(teacher)
    session.flush()
    return teachers


def create_subject(session: Session, teachers: list):
    subject_names = [
        "Introduction to Programming",
        "Data Structures and Algorithms",
        "Computer Networks",
        "Database Management Systems",
        "Software Engineering",
        "Operating Systems",
        "Artificial Intelligence",
    ]
    subjects = []
    for name in subject_names:
        subject = Subject(name=name, teacher=random.choice(teachers))
        session.add(subject)
        subjects.append(subject)
    session.flush()
    return subjects


def create_student(session: Session, groups: list):
    students = []
    for _ in range(100):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            group=random.choice(groups)
        )
        session.add(student)
        students.append(student)
    session.flush()
    return students


def create_grades(session: Session, students: list, subjects: list):
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()

    for student in students:
        num_grades = random.randint(10, 20)
        for _ in range(num_grades):
            subject = random.choice(subjects)
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=random.randint(60, 100),
                date_received=start_date
                + timedelta(
                    days=random.randint(
                        0, 
                        (end_date - start_date).days)
                ),
            )
            session.add(grade)
    session.flush()


if __name__ == "__main__":
    seed_database()