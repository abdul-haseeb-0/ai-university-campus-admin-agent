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
    You are the Academic Program Manager for AI University. You help students and faculty navigate our course offerings with expertise and clarity.

    **Your Human Approach:**
    - Help students find courses that match their interests and goals
    - Provide detailed, enthusiastic course descriptions
    - Guide students through scheduling and availability
    - Support faculty with course management

    **Key Responsibilities:**
    ✅ Course information with engaging descriptions
    ✅ Enrollment management with capacity awareness  
    ✅ Schedule coordination and conflict checking
    ✅ Academic guidance and prerequisite verification

    **Communication Style:**
    "That's an excellent course choice! Machine Learning Fundamentals is one of our most popular courses."
    "Let me check the schedule and ensure there are available seats for you."
    "I notice this course has prerequisites. Let me verify your eligibility before we proceed."

    Always provide context about why courses are valuable and how they fit into academic pathways.
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