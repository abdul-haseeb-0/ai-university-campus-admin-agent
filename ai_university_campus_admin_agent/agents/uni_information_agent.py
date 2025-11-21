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

campus_info_agent = Agent(
    model='gemini-2.0-flash-001',
    name='campus_information_agent',
    instruction=campus_info_instructions,
)

# ===========================================
# Course Information Agent

def read_course_information():
    """Read course information from JSON file"""
    try:
        with open('ai_university_campus_admin_agent/data/course_information.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Course information file not found."}
    except json.JSONDecodeError:
        return {"error": "Invalid course information file format."}

course_info_data = read_course_information()

course_info_instructions = f"""
You are the Course Information Agent of the AI University Campus Administration System.
Your primary responsibility is to provide accurate, detailed information about the university courses, 
including course descriptions, schedules, prerequisites, and academic programs.

Here is the course information:
{json.dumps(course_info_data, indent=2)}

Provide comprehensive information about course offerings, descriptions, schedules, prerequisites, 
credit hours, and academic programs. Help students understand course requirements and academic pathways.
"""

course_info_agent = Agent(
    model='gemini-2.0-flash-001',
    name='course_information_agent',
    instruction=course_info_instructions,
)

# ===========================================
# Fee Information Agent

def get_fee_information():
    """Read fee information from JSON file"""
    try:
        with open('ai_university_campus_admin_agent/data/fee_information.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Fee information file not found."}
    except json.JSONDecodeError:
        return {"error": "Invalid fee information file format."}

fee_information_data = get_fee_information()

fee_info_instructions = f"""
You are the Fee Information Agent of the AI University Campus Administration System.
Your primary responsibility is to provide accurate, detailed information about the university fee structures, 
payment plans, tuition costs, and financial policies.

Here is the fee information:
{json.dumps(fee_information_data, indent=2)}

Provide clear information about tuition fees, payment deadlines, payment methods, financial aid options, 
and university financial policies. Help students and parents understand the cost structure and payment requirements.
"""

fee_info_agent = Agent(
    model='gemini-2.0-flash-001',
    name='fee_information_agent',
    instruction=fee_info_instructions,
)

# ===========================================
# Main University Information Agent

instructions = """
You are the University Information Agent of the AI University Campus Administration System.
Your primary responsibility is to provide accurate, detailed information about the university campus, courses, and fees.

You have access to three specialized sub-agents:
1. Campus Information Agent: Provides details about campus departments, facilities, policies, and contacts.
2. Course Information Agent: Offers information on course descriptions, schedules, prerequisites, and academic programs.
3. Fee Information Agent: Delivers comprehensive fee information, cost calculations, and payment guidance.

When responding to user queries:
- Analyze the question to determine which specialized agent is best suited
- Delegate specific questions to the appropriate agent
- If a question spans multiple domains, coordinate responses from relevant agents
- Provide comprehensive, integrated answers when needed

Focus on delivering accurate, helpful information and guiding users to the right resources.
"""

uni_information_agent = Agent(
    model='gemini-2.0-flash-001',
    name='university_information_agent',  # Fixed duplicate name
    instruction=instructions,
    sub_agents=[campus_info_agent, course_info_agent, fee_info_agent],
)