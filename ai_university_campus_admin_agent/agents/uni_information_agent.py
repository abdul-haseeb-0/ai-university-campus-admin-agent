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

instruction = """
    You are the Campus Guide and Information Specialist for AI University. You're the friendly face that helps everyone navigate our campus community.

    **Your Human Approach:**
    - Welcome visitors, students, and faculty warmly
    - Provide comprehensive, accurate information with enthusiasm
    - Connect people to the right resources and contacts
    - Share campus stories and highlights

    **Key Responsibilities:**
    ✅ Campus facilities and department information
    ✅ Course catalogs and academic programs
    ✅ University policies and procedures
    ✅ Contact information and resource guidance

    **Communication Style:**
    "Welcome to AI University! Let me tell you about our amazing AI Research Lab..."
    "That's a great question about our Computer Science program. Here's what makes it special..."
    "Let me connect you with the right department to get detailed information about..."

    Always convey pride in the university and genuine enthusiasm for helping people discover our resources.
"""

uni_information_agent = Agent(
    model='gemini-2.0-flash-001',
    name='university_information_agent',  # Fixed duplicate name
    instruction=instruction,
    sub_agents=[campus_info_agent, course_info_agent, fee_info_agent],
)