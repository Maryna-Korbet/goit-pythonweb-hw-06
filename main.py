from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from database.db import SessionLocal
from entity.models import Student, Grade, Group, Subject


# 1. Find the 5 students with the highest average scores in all subjects.
def select_01(session: Session):
    query = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


# 2. Find the student with the highest GPA in a particular subject.
def select_02(session: Session, subject_id: int):
    stmt = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade, Student.id == Grade.student_id)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(stmt).first()


# 3. Find the average score in groups in a particular subject.
def select_03(session: Session, subject_id: int):
    stmt = (
        select(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
    )
    return session.execute(stmt).all()


# 4. Find the average score on the stream (across the entire grade table).
def select_04(session: Session):
    stmt = select(func.avg(Grade.grade).label("avg_grade"))
    return session.execute(stmt).scalar()


# 5. Find out what courses a particular teacher teaches.
def select_05(session: Session, teacher_id: int):
    stmt = (
        select(Subject.name)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalars().all()


# 6. Find a list of students in a specific group.
def select_06(session: Session, group_id: int):
    stmt = select(Student).where(Student.group_id == group_id)
    return session.execute(stmt).scalars().all()


# 7. Find the grades of students in a particular group in a particular subject.
def select_07(session: Session, group_id: int, subject_id: int):
    stmt = (
        select(Student.first_name, Student.last_name, Grade.grade)
        .join(Grade, Student.id == Grade.student_id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
    )
    return session.execute(stmt).all()


# Демонстрація запуску функцій:
if __name__ == "__main__":
    session = SessionLocal()
    try:
        print("Top 5 students with highest GPA:")
        for student, avg in select_01(session):
            print(f"{student.full_name} - {avg:.2f}")

        print("\nTop student in subject 1:")
        result = select_02(session, subject_id=1)
        if result:
            student, avg = result
            print(f"{student.full_name} - {avg:.2f}")
        else:
            print("No data found.")

        print("\nAverage score per group for subject 1:")
        for group_name, avg in select_03(session, subject_id=1):
            print(f"{group_name} - {avg:.2f}")

        print("\nAverage score across all grades:")
        print(f"{select_04(session):.2f}")

        print("\nSubjects taught by teacher 1:")
        for subject in select_05(session, teacher_id=1):
            print(subject)

        print("\nStudents in group 1:")
        for student in select_06(session, group_id=1):
            print(student.full_name)

        print("\nGrades for students in group 1 for subject 1:")
        for first_name, last_name, grade in select_07(session, group_id=1, subject_id=1):
            print(
                f"{first_name} {last_name}: {grade}"
            )

    finally:
        session.close()