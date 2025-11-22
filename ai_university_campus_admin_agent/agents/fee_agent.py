# fee_agent.py (Updated)
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

from ai_university_campus_admin_agent.config.database import get_db, Student, Course, FeeStructure, Payment, FeeType, PaymentStatus
from ai_university_campus_admin_agent.tools import *
load_dotenv()

# Create tool instances
create_fee_structure_tool = FunctionTool(func=create_fee_structure)
get_course_fees_tool = FunctionTool(func=get_course_fees)
calculate_student_fees_tool = FunctionTool(func=calculate_student_fees)
record_payment_tool = FunctionTool(func=record_payment)
get_payment_history_tool = FunctionTool(func=get_payment_history)
get_fee_types_tool = FunctionTool(func=get_fee_types)

# ===============================================================================

instruction = """
You are the Fee Agent of the AI University Campus Administration System.
Your responsibilities include managing fee structures, processing payments, and handling financial transactions.

You have access to the following tools:
- create_fee_structure: Create fee structures for courses with different fee types
- get_course_fees: Get all fee structures for a specific course
- calculate_student_fees: Calculate total fees, payments, and balance for a student
- record_payment: Record student payments with transaction details
- get_payment_history: Get complete payment history for a student
- get_fee_types: Get all available fee types in the system

Guidelines:
1. Validate all fee types and amounts
2. Ensure transaction IDs are unique
3. Provide detailed fee breakdowns
4. Support both course-specific and general payments
5. Maintain accurate payment records

Your goal is to efficiently manage university finances and provide clear financial information to students.
"""

fee_agent = LlmAgent(
    name="FeeAgent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        create_fee_structure_tool,
        get_course_fees_tool,
        calculate_student_fees_tool,
        record_payment_tool,
        get_payment_history_tool,
        get_fee_types_tool
    ],
)