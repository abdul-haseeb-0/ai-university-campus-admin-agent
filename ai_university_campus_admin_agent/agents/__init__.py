# ai_university_campus_admin_agent/agents/__init__.py

from .registration_agent import registration_agent
from .course_agent import course_agent
from .fee_agent import fee_agent
from .analyst_agent import analyst_agent
from .uni_information_agent import uni_information_agent

__all__ = [
    'registration_agent',
    'course_agent', 
    'fee_agent',
    'analyst_agent',
    'uni_information_agent'
]