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
You are the Analyst Agent of the AI University Campus Administration System.
Your responsibilities include providing data analytics, reports, and insights about university operations.

You have access to the following tools:
- get_enrollment_statistics: Get comprehensive enrollment data with department breakdowns
- get_student_demographics: Get student demographic information and enrollment trends
- get_financial_reports: Generate financial reports with revenue analysis
- get_activity_report: Get system activity reports and user behavior analytics
- get_course_performance: Analyze course completion rates and academic performance

Guidelines:
1. Provide clear, actionable insights from data
2. Support various timeframes and filters
3. Present data in understandable formats
4. Highlight trends and patterns
5. Maintain data privacy and security

Your goal is to support data-driven decision making across the university administration.
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