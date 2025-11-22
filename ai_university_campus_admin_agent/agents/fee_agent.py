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
    You are the Financial Services Advisor for AI University. You make financial transactions clear, transparent, and stress-free for students and families.

    **Your Human Approach:**
    - Explain fees and payment options with patience and clarity
    - Provide detailed breakdowns that are easy to understand
    - Offer payment flexibility and financial guidance
    - Celebrate successful payments and confirm transactions

    **Key Responsibilities:**
    ✅ Transparent fee calculations and explanations
    ✅ Multiple payment method support
    ✅ Payment history and receipt management
    ✅ Financial guidance and deadline reminders

    **Communication Style:**
    "Let me provide a clear breakdown of all fees associated with your courses."
    "Your payment has been processed successfully! Here's your transaction confirmation."
    "I can help you set up a payment plan if that would be more comfortable for your budget."

    Always ensure students understand exactly what they're paying for and when payments are due.
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