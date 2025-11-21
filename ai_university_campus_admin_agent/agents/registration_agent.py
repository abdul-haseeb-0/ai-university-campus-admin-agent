from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
from google.adk.models import LlmRequest

from google.genai.types import ThinkingConfig
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional    
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_

import datetime
from zoneinfo import ZoneInfo

# Conceptual Code: Using a Tool for Human Approval
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool

# Agent that prepares the request
# Conceptual Example: Defining Hierarchy
from google.adk.agents import LlmAgent, BaseAgent
from ai_university_campus_admin_agent.config.database import get_db


from ai_university_campus_admin_agent.models.models import Student

# ===============================================================================

# Registration Tools (CRUD)
# create_student()

def create_student(name: str, student_id: str, department: str, email: str) -> Dict[str, Any]:
    try:
        db: Session = next(get_db())
        new_student = Student(
            name=name,
            student_id=student_id,
            department=department,
            email=email,
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"status": "success",
            "student": {
                "id": new_student.id,
                "name": new_student.name,
                "student_id": new_student.student_id,
                "department": new_student.department,
                "email": new_student.email
                }
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

# get_student()
def get_student(student_id: str) -> Dict[str, Any]:
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            return {"status": "success",
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "student_id": student.student_id,
                    "department": student.department,
                    "email": student.email
                    }
                }
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# update_student()
def update_student(student_id: str, name: Optional[str] = None, department: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            if name:
                student.name = name
            if department:
                student.department = department
            if email:
                student.email = email
            student.updated_at = datetime.datetime.now(ZoneInfo("UTC"))
            db.commit()
            db.refresh(student)
            return {"status": "success",
                "student": {
                    "id": student.id,
                    "name": student.name,
                    "student_id": student.student_id,
                    "department": student.department,
                    "email": student.email
                    }
                }
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# delete_student()
def delete_student(student_id: str) -> Dict[str, Any]:
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            db.delete(student)
            db.commit()
            return {"status": "success", "message": "Student deleted successfully"}
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# enroll_course()
def enroll_course(student_id: str, course_code: str) -> Dict[str, Any]:
    try:
        db: Session = next(get_db())
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            # Assuming a many-to-many relationship between students and courses
            # This is a placeholder for actual enrollment logic
            return {"status": "success", "message": f"Student {student_id} enrolled in course {course_code}"}
        else:
            return {"status": "error", "message": "Student not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}





# ===============================================================================
instruction = """
You are the Registration Agent of the AI University Campus Administration System. Your responsibilities include managing student registrations, updating student information, and handling course enrollments. You will utilize various tools to perform CRUD operations on student records and manage course enrollments effectively.
You have access to the following tools:
- create_student(name: str, student_id: str, department: str, email: str) -> Dict[str, Any]: Create a new student record in the database.
- get_student(student_id: str) -> Dict[str, Any]: Retrieve student information based on the student ID.
- update_student(student_id: str, name: Optional[str] = None, department: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]: Update existing student information.
- delete_student(student_id: str) -> Dict[str, Any]: Delete a student record from the database.
- enroll_course(student_id: str, course_code: str) -> Dict[str, Any]: Enroll a student in a specified course.
Your goal is to assist with student registration processes, ensuring that all student data is accurately maintained and
Ensure that all operations are performed accurately and efficiently, maintaining the integrity of student data. Use the provided tools to execute these tasks as needed.
"""

registeration_agent = LlmAgent(
    name="RegistrationAgent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[create_student, get_student, update_student, delete_student, enroll_course],
    )