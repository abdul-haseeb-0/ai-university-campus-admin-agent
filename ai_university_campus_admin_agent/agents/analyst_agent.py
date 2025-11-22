# analyst_agent.py (Updated)
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
from sqlalchemy import func, desc, case
import datetime
from zoneinfo import ZoneInfo
from ai_university_campus_admin_agent.config.database import get_db,FeeStructure, Student, Course, Registration, Payment, Department, ActivityLog
from ai_university_campus_admin_agent.tools import *

load_dotenv()

# Create tool instances
get_enrollment_statistics_tool = FunctionTool(func=get_enrollment_statistics)
get_student_demographics_tool = FunctionTool(func=get_student_demographics)
get_financial_reports_tool = FunctionTool(func=get_financial_reports)
get_activity_report_tool = FunctionTool(func=get_activity_report)
get_course_performance_tool = FunctionTool(func=get_course_performance)

# ===============================================================================

instruction = """
    You are the Data Insights Specialist for AI University. You transform complex data into actionable insights that help everyone make better decisions.

    **Your Human Approach:**
    - Present data in clear, understandable formats
    - Highlight important trends and patterns
    - Provide context for what the numbers mean
    - Offer practical recommendations based on insights

    **Key Responsibilities:**
    ✅ Enrollment trends and forecasting
    ✅ Financial performance and revenue analytics
    ✅ Student success and course performance metrics
    ✅ Operational efficiency and resource utilization

    **Communication Style:**
    "Here's what the enrollment data shows us for this semester..."
    "This interesting trend suggests we might want to consider..."
    "Based on the performance metrics, I recommend..."

    Always connect data to real-world implications and opportunities for improvement.
"""

analyst_agent = LlmAgent(
    name="AnalystAgent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        get_enrollment_statistics_tool,
        get_student_demographics_tool,
        get_financial_reports_tool,
        get_activity_report_tool,
        get_course_performance_tool
    ],
)