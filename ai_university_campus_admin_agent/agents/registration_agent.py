# registration_agent.py (Updated)
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import ThinkingConfig, GenerateContentConfig
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional    
import uuid
from sqlalchemy.orm import Session
import datetime
from zoneinfo import ZoneInfo

from ai_university_campus_admin_agent.config.database import get_db, Student, Registration, Course, ActivityLog, ActivityType, RegistrationStatus

load_dotenv()

# ===============================================================================
# Registration Tools (CRUD Operations)

def create_student(name: str, student_id: str, department: str, email: str, phone: Optional[str] = None, address: Optional[str] = None) -> Dict[str, Any]:
    """Create a new student record in the database"""
    try:
        db: Session = next(get_db())
        
        # Check if student already exists
        existing_student = db.query(Student).filter(
            (Student.student_id == student_id) | (Student.email == email)
        ).first()
        
        if existing_student:
            return {"status": "error", "message": "Student ID or email already exists"}
        
        new_student = Student(
            name=name,
            student_id=student_id,
            department=department,
            email=email,
            phone=phone,
            address=address,
            enrollment_date=datetime.datetime.now(ZoneInfo("UTC")),
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        
        # Log activity
        activity_log = ActivityLog(
            student_id=student_id,
            activity_type=ActivityType.PROFILE_UPDATE,
            description="Student profile created",
            timestamp=datetime.datetime.now(ZoneInfo("UTC"))
        )
        db.add(activity_log)
        db.commit()
        
        return {
            "status": "success",
            "message": "Student created successfully",
            "student": {
                "id": new_student.id,
                "name": new_student.name,
                "student_id": new_student.student_id,
                "department": new_student.department,
                "email": new_student.email,
                "phone": new_student.phone
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_student(student_id: str) -> Dict[str, Any]:
    """Retrieve student information based on student ID"""
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        
        if student:
            return {
                "status": "success",
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "student_id": student.student_id,
                    "department": student.department,
                    "email": student.email,
                    "phone": student.phone,
                    "address": student.address,
                    "enrollment_date": student.enrollment_date.isoformat() if student.enrollment_date else None,
                    "is_active": student.is_active
                }
            }
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_student(student_id: str, name: Optional[str] = None, department: Optional[str] = None, 
                  email: Optional[str] = None, phone: Optional[str] = None, address: Optional[str] = None) -> Dict[str, Any]:
    """Update existing student information"""
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        
        if student:
            updates = []
            if name and name != student.name:
                student.name = name
                updates.append("name")
            if department and department != student.department:
                student.department = department
                updates.append("department")
            if email and email != student.email:
                student.email = email
                updates.append("email")
            if phone is not None:
                student.phone = phone
                updates.append("phone")
            if address is not None:
                student.address = address
                updates.append("address")
            
            student.updated_at = datetime.datetime.now(ZoneInfo("UTC"))
            db.commit()
            db.refresh(student)
            
            # Log activity
            if updates:
                activity_log = ActivityLog(
                    student_id=student_id,
                    activity_type=ActivityType.PROFILE_UPDATE,
                    description=f"Student profile updated: {', '.join(updates)}",
                    timestamp=datetime.datetime.now(ZoneInfo("UTC"))
                )
                db.add(activity_log)
                db.commit()
            
            return {
                "status": "success",
                "message": "Student updated successfully",
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "student_id": student.student_id,
                    "department": student.department,
                    "email": student.email,
                    "phone": student.phone
                }
            }
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_student(student_id: str) -> Dict[str, Any]:
    """Delete a student record from the database"""
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        
        if student:
            # Check for active registrations
            active_registrations = db.query(Registration).filter(
                Registration.student_id == student_id,
                Registration.status == RegistrationStatus.ACTIVE
            ).count()
            
            if active_registrations > 0:
                return {
                    "status": "error", 
                    "message": f"Cannot delete student with {active_registrations} active course registrations"
                }
            
            db.delete(student)
            db.commit()
            
            return {"status": "success", "message": "Student deleted successfully"}
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def enroll_course(student_id: str, course_code: str) -> Dict[str, Any]:
    """Enroll a student in a specified course"""
    try:
        db: Session = next(get_db())
        
        # Check if student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        # Check if course exists and has capacity
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        if not course.is_active:
            return {"status": "error", "message": "Course is not active"}
        
        if course.current_enrollment >= course.max_capacity:
            return {"status": "error", "message": "Course is full"}
        
        # Check if already enrolled
        existing_registration = db.query(Registration).filter(
            Registration.student_id == student_id,
            Registration.course_id == course.id
        ).first()
        
        if existing_registration:
            return {"status": "error", "message": "Student is already enrolled in this course"}
        
        # Create registration
        new_registration = Registration(
            student_id=student_id,
            course_id=course.id,
            registration_date=datetime.datetime.now(ZoneInfo("UTC")),
            status=RegistrationStatus.ACTIVE,
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        
        # Update course enrollment count
        course.current_enrollment += 1
        
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        
        # Log activity
        activity_log = ActivityLog(
            student_id=student_id,
            activity_type=ActivityType.COURSE_REGISTRATION,
            description=f"Enrolled in course: {course.course_code} - {course.course_name}",
            timestamp=datetime.datetime.now(ZoneInfo("UTC"))
        )
        db.add(activity_log)
        db.commit()
        
        return {
            "status": "success",
            "message": "Successfully enrolled in course",
            "registration": {
                "id": new_registration.id,
                "student_id": new_registration.student_id,
                "course_code": course.course_code,
                "course_name": course.course_name,
                "status": new_registration.status.value
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_student_registrations(student_id: str) -> Dict[str, Any]:
    """Get all course registrations for a student"""
    try:
        db: Session = next(get_db())
        
        registrations = db.query(Registration, Course).join(
            Course, Registration.course_id == Course.id
        ).filter(Registration.student_id == student_id).all()
        
        result = []
        for registration, course in registrations:
            result.append({
                "course_code": course.course_code,
                "course_name": course.course_name,
                "registration_date": registration.registration_date.isoformat(),
                "status": registration.status.value,
                "credits": course.credits,
                "instructor": course.instructor
            })
        
        return {
            "status": "success",
            "student_id": student_id,
            "registrations": result,
            "total_courses": len(result)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Create tool instances
create_student_tool = FunctionTool(func=create_student)
get_student_tool = FunctionTool(func=get_student)
update_student_tool = FunctionTool(func=update_student)
delete_student_tool = FunctionTool(func=delete_student)
enroll_course_tool = FunctionTool(func=enroll_course)
get_student_registrations_tool = FunctionTool(func=get_student_registrations)

# ===============================================================================

instruction = """
You are the Registration Agent of the AI University Campus Administration System. 
Your responsibilities include managing student registrations, updating student information, and handling course enrollments.

You have access to the following tools:
- create_student: Create a new student record with name, student_id, department, email, and optional phone/address
- get_student: Retrieve complete student information by student ID
- update_student: Update student information (name, department, email, phone, address)
- delete_student: Delete a student record (only if no active course registrations)
- enroll_course: Enroll a student in a specified course
- get_student_registrations: Get all course registrations for a student

Guidelines:
1. Always verify student exists before performing operations
2. Check course availability before enrollment
3. Maintain data integrity and prevent duplicates
4. Provide clear success/error messages
5. Log important activities for audit purposes

Your goal is to assist with student registration processes, ensuring all student data is accurately maintained and operations are performed efficiently.
"""

registration_agent = LlmAgent(
    name="RegistrationAgent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        create_student_tool, 
        get_student_tool, 
        update_student_tool, 
        delete_student_tool, 
        enroll_course_tool,
        get_student_registrations_tool
    ],
)