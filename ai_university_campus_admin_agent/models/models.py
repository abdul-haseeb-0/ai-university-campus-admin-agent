from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    course = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="student", cascade="all, delete-orphan")
    course_registrations = relationship("CourseRegistration", back_populates="student", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="student", cascade="all, delete-orphan")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="activity_logs")

class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    course_code = Column(String(20), nullable=False)
    course_name = Column(String(100), nullable=False)
    semester = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="course_registrations")