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
from ai_university_campus_admin_agent.tools import *
load_dotenv()

# ===============================================================================
# Registration Tools (CRUD Operations)


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