from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
from google.adk.models import LlmRequest

from google.genai.types import ThinkingConfig
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional    
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_

import datetime
from zoneinfo import ZoneInfo

# Conceptual Code: Using a Tool for Human Approval
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
# from agents.registration import registeration_agent
 
# Agent that prepares the request
# Conceptual Example: Defining Hierarchy
from google.adk.agents import LlmAgent, BaseAgent

from ai_university_campus_admin_agent.agents.registration_agent import registeration_agent
# ===============================================================================

root_agent = LlmAgent(
    name="orchestration_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are the Orchestration Agent of the AI University Campus Administration System. Your responsibilities include managing student registrations, updating student information, and handling course enrollments. You will utilize various tools to perform CRUD operations on student records and manage course enrollments effectively.
    you have access to the following subagents:
    registeration_agent: Handles student registrations and updates.
    """,
    sub_agents=[registeration_agent]
)