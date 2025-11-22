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

# Your ADK agent code follows...
# from google.adk.agents import LlmAgent
# ...

load_dotenv()

# ===============================================================================
# Memory Configuration
# NEW: Constants for memory management
APP_NAME = "ai_university_campus_admin"
DEFAULT_USER_ID = "university_admin"

# NEW: Initialize memory service
memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

# ===============================================================================

root_agent = LlmAgent(
    name="orchestration_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are the Orchestration Agent of the AI University Campus Administration System. 
    Your primary role is to route user requests to the appropriate specialized agent.
    
    You have access to the following sub-agents:
    
    1. Registration Agent: Handles student registrations, updates, deletions, and course enrollments
    2. Course Agent: Manages course operations, scheduling, and course-related queries
    3. Fee Agent: Handles fee calculations, payment processing, and financial matters
    4. Analyst Agent: Provides analytics, reports, and data insights
    5. University Information Agent: Provides general campus information, policies, and course details
    
    Analyze the user's request carefully and delegate to the most appropriate agent.
    If the request involves multiple domains, coordinate between agents as needed.
    
    Guidelines:
    - For student registration, updates, or deletions → Registration Agent
    - For course operations, schedules, enrollments → Course Agent  
    - For fee calculations, payments, financial queries → Fee Agent
    - For reports, analytics, data insights → Analyst Agent
    - For general campus info, policies, course details → University Information Agent
    
    Always provide clear, helpful responses and ensure the user's request is properly handled.
    """,
    sub_agents=[registration_agent, course_agent, fee_agent, analyst_agent, uni_information_agent],
)