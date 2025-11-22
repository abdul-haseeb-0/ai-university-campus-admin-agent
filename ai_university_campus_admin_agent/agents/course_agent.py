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
from ai_university_campus_admin_agent.tools import *
load_dotenv()

# ===============================================================================
# Course Management Tools


# Create tool instances
create_course_tool = FunctionTool(func=create_course)
get_course_tool = FunctionTool(func=get_course)
get_all_courses_tool = FunctionTool(func=get_all_courses)
update_course_tool = FunctionTool(func=update_course)
get_course_enrollments_tool = FunctionTool(func=get_course_enrollments)
drop_course_tool = FunctionTool(func=drop_course)

# ===============================================================================

instruction = """
You are the Course Agent of the AI University Campus Administration System.
Your responsibilities include managing courses, handling course operations, and providing course-related information.

You have access to the following tools:
- create_course: Create a new course with code, name, credits, department, and optional details
- get_course: Retrieve detailed course information by course code
- get_all_courses: Get all courses with optional filters (department, semester, active status)
- update_course: Update course information and settings
- get_course_enrollments: Get all students enrolled in a specific course
- drop_course: Drop a student from a course

Guidelines:
1. Ensure course codes are unique
2. Maintain course capacity limits
3. Provide comprehensive course information
4. Handle enrollment changes properly
5. Support department-based course filtering

Your goal is to efficiently manage the university's course catalog and support academic operations.
"""

course_agent = LlmAgent(
    name="CourseAgent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        create_course_tool,
        get_course_tool,
        get_all_courses_tool,
        update_course_tool,
        get_course_enrollments_tool,
        drop_course_tool
    ],
)