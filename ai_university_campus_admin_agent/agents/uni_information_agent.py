# uni_information_agent.py (Updated - fix the duplicate Agent definition)
import os
import json
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()

# =====================================
# Campus Information Agent

def read_campus_information():
    """Read campus information from JSON file"""
    try:
        with open('ai_university_campus_admin_agent/data/university_information.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Campus information file not found."}
    except json.JSONDecodeError:
        return {"error": "Invalid campus information file format."}

campus_info_data = read_campus_information()

campus_info_instructions = f"""
You are the Campus Information Agent of the AI University Campus Administration System.
Your primary responsibility is to provide accurate, detailed information about the university campus, 
including departments, facilities, policies, and contacts.

Here is the campus information:
{json.dumps(campus_info_data, indent=2)}

Provide comprehensive and helpful responses about campus facilities, departments, policies, contacts, 
and general university information. If you cannot find specific information in the provided data, 
be honest about the limitations.
"""

uni_information_agent = Agent(
    model='gemini-2.0-flash-001',
    name='campus_information_agent',
    instruction=campus_info_instructions,
)