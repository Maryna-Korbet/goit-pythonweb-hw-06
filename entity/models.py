"""
This module defines SQLAlchemy ORM models for a school management system.
It includes classes for groups, students, teachers, subjects, and grades.
"""
from datetime import datetime
# from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, func
from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy.ext.hybrid import hybrid_property
from typing import List


class Base(DeclarativeBase):
    """Base class for all models using SQLAlchemy ORM."""
    pass


class Group(Base):
    """
    Represents a student group.

    Attributes:
        id: Primary key.
        name: Name of the group.
        students: List of students in the group.
        grades: Grades associated with this group.
    """
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    students: Mapped[List["Student"]] = relationship(back_populates="group")

    """ @hybrid_property
    def count(self):
        Returns the number of students in the group.
        return len(self.students)

    @count.expression
    def count(cls):
        return func.count(cls.students) """


class Student(Base):
    """
    Represents a student.

    Attributes:
        id: Primary key.
        first_name, last_name, email, phone: Contact details.
        group_id: Foreign key to Group.
        grades: List of grades for the student.
    """
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("groups.id", ondelete="SET NULL"),
        nullable=False
    )

    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[List["Grade"]] = relationship(
        back_populates="student", 
        cascade="all, delete-orphan"
    )

    """ @hybrid_property
    def full_name(self):
        Returns full name of the teacher.
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name) """


class Teacher(Base):
    """
    Represents a teacher.

    Attributes:
        id: Primary key.
        first_name, last_name, email, phone: Contact details.
        subjects: List of subjects taught by the teacher.
    """
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    subjects: Mapped[List["Subject"]] = relationship(
        "Subject", 
        back_populates="teacher"
    )

    """ @hybrid_property
    def full_name(self):
        Returns full name of the teacher.
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name) """


class Subject(Base):
    """
    Represents a school subject.

    Attributes:
        id: Primary key.
        name: Name of the subject.
        teacher_id: Foreign key to Teacher.
    """
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    teacher_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=False
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    grades: Mapped[List["Grade"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan"
    )


class Grade(Base):
    """
    Represents a grade assigned to a student for a subject.

    Attributes:
        id: Primary key.
        student_id: Foreign key to Student.
        subject_id: Foreign key to Subject.
        grade: The numeric grade.
        date_received: Date the grade was given.
    """
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False
    )
    grade: Mapped[float] = mapped_column(Float, nullable=False)
    date_received: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")
