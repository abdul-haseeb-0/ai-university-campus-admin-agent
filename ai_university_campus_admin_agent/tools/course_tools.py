# course_agent.py (Updated)
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import ThinkingConfig, GenerateContentConfig
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional    
from sqlalchemy.orm import Session
import datetime
from zoneinfo import ZoneInfo

from ai_university_campus_admin_agent.config.database import get_db, Course, Registration, Student, RegistrationStatus

load_dotenv()

def create_course(course_code: str, course_name: str, credits: int, department: str, 
                 description: Optional[str] = None, semester: Optional[str] = None,
                 year: Optional[int] = None, max_capacity: int = 30, instructor: Optional[str] = None,
                 schedule: Optional[str] = None, location: Optional[str] = None, prerequisites: Optional[str] = None) -> Dict[str, Any]:
    """Create a new course in the database"""
    try:
        db: Session = next(get_db())
        
        # Check if course code already exists
        existing_course = db.query(Course).filter(Course.course_code == course_code).first()
        if existing_course:
            return {"status": "error", "message": "Course code already exists"}
        
        new_course = Course(
            course_code=course_code,
            course_name=course_name,
            description=description,
            credits=credits,
            department=department,
            semester=semester,
            year=year,
            max_capacity=max_capacity,
            current_enrollment=0,
            instructor=instructor,
            schedule=schedule,
            location=location,
            prerequisites=prerequisites,
            is_active=True,
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        
        return {
            "status": "success",
            "message": "Course created successfully",
            "course": {
                "id": new_course.id,
                "course_code": new_course.course_code,
                "course_name": new_course.course_name,
                "credits": new_course.credits,
                "department": new_course.department,
                "instructor": new_course.instructor,
                "max_capacity": new_course.max_capacity
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_course(course_code: str) -> Dict[str, Any]:
    """Retrieve course information by course code"""
    try:
        db: Session = next(get_db())
        course = db.query(Course).filter(Course.course_code == course_code).first()
        
        if course:
            return {
                "status": "success",
                "course": {
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "description": course.description,
                    "credits": course.credits,
                    "department": course.department,
                    "semester": course.semester,
                    "year": course.year,
                    "max_capacity": course.max_capacity,
                    "current_enrollment": course.current_enrollment,
                    "available_seats": course.max_capacity - course.current_enrollment,
                    "instructor": course.instructor,
                    "schedule": course.schedule,
                    "location": course.location,
                    "prerequisites": course.prerequisites,
                    "is_active": course.is_active
                }
            }
        else:
            return {"status": "error", "message": "Course not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_courses(department: Optional[str] = None, semester: Optional[str] = None, 
                   active_only: bool = True) -> Dict[str, Any]:
    """Get all courses with optional filters"""
    try:
        db: Session = next(get_db())
        
        query = db.query(Course)
        
        if department:
            query = query.filter(Course.department == department)
        if semester:
            query = query.filter(Course.semester == semester)
        if active_only:
            query = query.filter(Course.is_active == True)
        
        courses = query.all()
        
        result = []
        for course in courses:
            result.append({
                "course_code": course.course_code,
                "course_name": course.course_name,
                "credits": course.credits,
                "department": course.department,
                "semester": course.semester,
                "year": course.year,
                "current_enrollment": course.current_enrollment,
                "max_capacity": course.max_capacity,
                "available_seats": course.max_capacity - course.current_enrollment,
                "instructor": course.instructor,
                "schedule": course.schedule,
                "is_active": course.is_active
            })
        
        return {
            "status": "success",
            "courses": result,
            "total_courses": len(result),
            "filters": {
                "department": department,
                "semester": semester,
                "active_only": active_only
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_course(course_code: str, course_name: Optional[str] = None, credits: Optional[int] = None,
                 department: Optional[str] = None, description: Optional[str] = None,
                 max_capacity: Optional[int] = None, instructor: Optional[str] = None,
                 schedule: Optional[str] = None, location: Optional[str] = None,
                 is_active: Optional[bool] = None) -> Dict[str, Any]:
    """Update course information"""
    try:
        db: Session = next(get_db())
        course = db.query(Course).filter(Course.course_code == course_code).first()
        
        if course:
            updates = []
            if course_name and course_name != course.course_name:
                course.course_name = course_name
                updates.append("course_name")
            if credits is not None and credits != course.credits:
                course.credits = credits
                updates.append("credits")
            if department and department != course.department:
                course.department = department
                updates.append("department")
            if description is not None:
                course.description = description
                updates.append("description")
            if max_capacity is not None and max_capacity != course.max_capacity:
                if max_capacity < course.current_enrollment:
                    return {"status": "error", "message": "New capacity cannot be less than current enrollment"}
                course.max_capacity = max_capacity
                updates.append("max_capacity")
            if instructor is not None:
                course.instructor = instructor
                updates.append("instructor")
            if schedule is not None:
                course.schedule = schedule
                updates.append("schedule")
            if location is not None:
                course.location = location
                updates.append("location")
            if is_active is not None and is_active != course.is_active:
                course.is_active = is_active
                updates.append("is_active")
            
            course.updated_at = datetime.datetime.now(ZoneInfo("UTC"))
            db.commit()
            db.refresh(course)
            
            return {
                "status": "success",
                "message": f"Course updated successfully. Updated fields: {', '.join(updates)}" if updates else "No changes made",
                "course": {
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "credits": course.credits,
                    "department": course.department,
                    "max_capacity": course.max_capacity,
                    "current_enrollment": course.current_enrollment,
                    "is_active": course.is_active
                }
            }
        else:
            return {"status": "error", "message": "Course not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_course_enrollments(course_code: str) -> Dict[str, Any]:
    """Get all students enrolled in a course"""
    try:
        db: Session = next(get_db())
        
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        enrollments = db.query(Registration, Student).join(
            Student, Registration.student_id == Student.student_id
        ).filter(
            Registration.course_id == course.id,
            Registration.status == RegistrationStatus.ACTIVE
        ).all()
        
        result = []
        for registration, student in enrollments:
            result.append({
                "student_id": student.student_id,
                "student_name": student.name,
                "department": student.department,
                "email": student.email,
                "registration_date": registration.registration_date.isoformat()
            })
        
        return {
            "status": "success",
            "course_code": course_code,
            "course_name": course.course_name,
            "enrollments": result,
            "total_students": len(result),
            "capacity": f"{len(result)}/{course.max_capacity}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def drop_course(student_id: str, course_code: str) -> Dict[str, Any]:
    """Drop a student from a course"""
    try:
        db: Session = next(get_db())
        
        # Check if student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        # Check if course exists
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        # Find registration
        registration = db.query(Registration).filter(
            Registration.student_id == student_id,
            Registration.course_id == course.id
        ).first()
        
        if not registration:
            return {"status": "error", "message": "Student is not enrolled in this course"}
        
        if registration.status != RegistrationStatus.ACTIVE:
            return {"status": "error", "message": f"Student registration status is {registration.status.value}, cannot drop"}
        
        # Update registration status and course enrollment
        registration.status = RegistrationStatus.DROPPED
        registration.updated_at = datetime.datetime.now(ZoneInfo("UTC"))
        
        course.current_enrollment -= 1
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"Student {student_id} successfully dropped from {course_code}",
            "details": {
                "student_name": student.name,
                "course_name": course.course_name,
                "remaining_seats": course.max_capacity - course.current_enrollment
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
