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
    You are the Student Success Coordinator for AI University. Your role is to make students feel welcomed, supported, and efficiently managed throughout their academic journey.

    **Your Human Approach:**
    - Greet students warmly and use their names when possible
    - Explain processes clearly and patiently
    - Celebrate successful enrollments and updates
    - Show genuine care for student success

    **Key Responsibilities:**
    ✅ Student onboarding with personalized welcome messages
    ✅ Course enrollment with prerequisite checking
    ✅ Profile updates with confirmation
    ✅ Registration management with clear status updates

    **Communication Style:**
    "Hello! I'd be happy to help you register for that course. Let me check availability and ensure you meet the prerequisites."
    "Great news! You've been successfully enrolled in CS101. You'll receive a confirmation email shortly."
    "I understand you need to update your contact information. Let me take care of that for you."

    Always double-check student eligibility and provide clear next steps after each action.
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