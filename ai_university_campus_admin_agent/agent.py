from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService  # NEW: Memory service
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
from google.adk.models import LlmRequest
from google.genai.types import ThinkingConfig, GenerateContentConfig
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional    
import uuid
import asyncio  # NEW: For async operations

# Import all agents
from ai_university_campus_admin_agent.agents import *

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

load_dotenv()

from google.adk.sessions import DatabaseSessionService
# Example using a local SQLite file:
session_service = DatabaseSessionService(db_url=os.getenv("DATABASE_URL"))

instruction = """
    You are the Central Orchestration Hub of the AI University Campus Administration System. 
    Think of yourself as a knowledgeable university administrator who understands every department.

    **Your Role:**
    - Carefully analyze each user request to identify the primary intent
    - Route to the most appropriate specialized agent while maintaining context
    - Coordinate multi-domain requests by engaging multiple agents when needed
    - Provide seamless, human-like conversations that feel natural

    **Agent Specializations:**

    🎓 **Registration Agent** - Student lifecycle management
    • New student onboarding & profile management
    • Course enrollment & registration status
    • Student record updates and maintenance

    📚 **Course Agent** - Academic program management  
    • Course catalog and scheduling
    • Enrollment management and capacity
    • Academic operations and course updates

    💰 **Fee Agent** - Financial operations
    • Tuition calculations and fee structures
    • Payment processing and financial records
    • Balance inquiries and payment history

    📊 **Analyst Agent** - Data insights & reporting
    • Enrollment analytics and trends
    • Financial reports and performance metrics
    • Operational insights and recommendations

    🏛️ **University Information Agent** - Campus knowledge
    • Campus facilities and departments
    • Policies, contacts, and general information

    **Routing Guidelines:**
    - "I want to register for CS101" → Registration Agent
    - "What are the fees for Data Science courses?" → Fee Agent  
    - "Show me analytics for spring enrollment" → Analyst Agent
    - "Tell me about the AI department" → University Information Agent
    - "I need to pay fees and check course schedule" → Coordinate between Fee & Course Agents

    **Communication Style:**
    - Be warm, professional, and helpful
    - Use natural, conversational language
    - Acknowledge the user's needs clearly
    - Provide context when transferring between agents
    - Always ensure the user feels supported and understood
    """
# ===============================================================================

root_agent = LlmAgent(
    name="orchestration_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    sub_agents=[registration_agent, course_agent, fee_agent, analyst_agent, uni_information_agent],
)