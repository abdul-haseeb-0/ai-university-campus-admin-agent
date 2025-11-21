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

load_dotenv()

# ===============================================================================
# Analytics Tools

def get_enrollment_statistics(department: Optional[str] = None, semester: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive enrollment statistics"""
    try:
        db: Session = next(get_db())
        
        # Base query for courses
        course_query = db.query(Course)
        if department:
            course_query = course_query.filter(Course.department == department)
        if semester:
            course_query = course_query.filter(Course.semester == semester)
        
        courses = course_query.all()
        
        total_courses = len(courses)
        total_capacity = sum(course.max_capacity for course in courses)
        total_enrollment = sum(course.current_enrollment for course in courses)
        
        # Enrollment by department
        dept_enrollment = db.query(
            Course.department,
            func.sum(Course.current_enrollment).label('total_enrollment'),
            func.sum(Course.max_capacity).label('total_capacity')
        ).group_by(Course.department).all()
        
        department_stats = []
        for dept, enrollment, capacity in dept_enrollment:
            utilization = (enrollment / capacity * 100) if capacity > 0 else 0
            department_stats.append({
                "department": dept,
                "enrollment": enrollment,
                "capacity": capacity,
                "utilization_rate": round(utilization, 2)
            })
        
        # Top enrolled courses
        top_courses = db.query(
            Course.course_code,
            Course.course_name,
            Course.current_enrollment,
            Course.max_capacity
        ).order_by(desc(Course.current_enrollment)).limit(10).all()
        
        top_courses_list = []
        for course in top_courses:
            utilization = (course.current_enrollment / course.max_capacity * 100) if course.max_capacity > 0 else 0
            top_courses_list.append({
                "course_code": course.course_code,
                "course_name": course.course_name,
                "enrollment": course.current_enrollment,
                "capacity": course.max_capacity,
                "utilization": round(utilization, 2)
            })
        
        return {
            "status": "success",
            "statistics": {
                "total_courses": total_courses,
                "total_capacity": total_capacity,
                "total_enrollment": total_enrollment,
                "overall_utilization": round((total_enrollment / total_capacity * 100), 2) if total_capacity > 0 else 0,
                "available_seats": total_capacity - total_enrollment
            },
            "department_breakdown": department_stats,
            "top_courses": top_courses_list,
            "filters_applied": {
                "department": department,
                "semester": semester
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_student_demographics() -> Dict[str, Any]:
    """Get student demographic statistics"""
    try:
        db: Session = next(get_db())
        
        # Total students
        total_students = db.query(Student).count()
        active_students = db.query(Student).filter(Student.is_active == True).count()
        
        # Students by department
        students_by_dept = db.query(
            Student.department,
            func.count(Student.id).label('count')
        ).group_by(Student.department).all()
        
        department_stats = []
        for dept, count in students_by_dept:
            percentage = (count / total_students * 100) if total_students > 0 else 0
            department_stats.append({
                "department": dept,
                "student_count": count,
                "percentage": round(percentage, 2)
            })
        
        # Enrollment trends (last 6 months)
        six_months_ago = datetime.datetime.now(ZoneInfo("UTC")) - datetime.timedelta(days=180)
        
        recent_enrollments = db.query(
            func.strftime('%Y-%m', Student.enrollment_date).label('month'),
            func.count(Student.id).label('count')
        ).filter(
            Student.enrollment_date >= six_months_ago
        ).group_by('month').order_by('month').all()
        
        enrollment_trends = []
        for month, count in recent_enrollments:
            enrollment_trends.append({
                "month": month,
                "new_students": count
            })
        
        return {
            "status": "success",
            "demographics": {
                "total_students": total_students,
                "active_students": active_students,
                "inactive_students": total_students - active_students
            },
            "department_distribution": department_stats,
            "enrollment_trends": enrollment_trends
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_financial_reports(timeframe: str = "current_semester") -> Dict[str, Any]:
    """Get financial reports and revenue statistics"""
    try:
        db: Session = next(get_db())
        
        # Define time filters
        now = datetime.datetime.now(ZoneInfo("UTC"))
        if timeframe == "current_semester":
            start_date = now.replace(month=1 if now.month <= 6 else 7, day=1)
        elif timeframe == "last_30_days":
            start_date = now - datetime.timedelta(days=30)
        elif timeframe == "last_90_days":
            start_date = now - datetime.timedelta(days=90)
        else:  # all_time
            start_date = datetime.datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC"))
        
        # Total revenue
        total_revenue = db.query(func.sum(Payment.amount_paid)).filter(
            Payment.payment_date >= start_date,
            Payment.status == 'paid'
        ).scalar() or 0
        
        # Revenue by fee type
        revenue_by_type = db.query(
            FeeStructure.fee_type,
            func.sum(Payment.amount_paid).label('revenue')
        ).join(
            Payment, Payment.fee_structure_id == FeeStructure.id
        ).filter(
            Payment.payment_date >= start_date,
            Payment.status == 'paid'
        ).group_by(FeeStructure.fee_type).all()
        
        fee_type_revenue = []
        for fee_type, revenue in revenue_by_type:
            percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
            fee_type_revenue.append({
                "fee_type": fee_type.value,
                "revenue": revenue,
                "percentage": round(percentage, 2)
            })
        
        # Payment methods distribution
        payment_methods = db.query(
            Payment.payment_method,
            func.count(Payment.id).label('count'),
            func.sum(Payment.amount_paid).label('amount')
        ).filter(
            Payment.payment_date >= start_date,
            Payment.status == 'paid'
        ).group_by(Payment.payment_method).all()
        
        method_distribution = []
        for method, count, amount in payment_methods:
            method_distribution.append({
                "method": method,
                "transaction_count": count,
                "total_amount": amount
            })
        
        # Outstanding payments
        outstanding_query = """
        SELECT SUM(fs.amount) - COALESCE(SUM(p.amount_paid), 0) as outstanding
        FROM fee_structures fs
        LEFT JOIN payments p ON fs.id = p.fee_structure_id
        WHERE fs.is_active = 1
        AND (p.id IS NULL OR p.status = 'paid')
        """
        
        # This is a simplified calculation - in production, you'd want a more accurate query
        total_fees = db.query(func.sum(FeeStructure.amount)).filter(
            FeeStructure.is_active == True
        ).scalar() or 0
        
        total_payments = db.query(func.sum(Payment.amount_paid)).filter(
            Payment.status == 'paid'
        ).scalar() or 0
        
        outstanding_balance = total_fees - total_payments
        
        return {
            "status": "success",
            "timeframe": timeframe,
            "financial_summary": {
                "total_revenue": total_revenue,
                "outstanding_balance": outstanding_balance,
                "collection_rate": round((total_payments / total_fees * 100), 2) if total_fees > 0 else 0
            },
            "revenue_by_fee_type": fee_type_revenue,
            "payment_methods": method_distribution
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_activity_report(days: int = 30) -> Dict[str, Any]:
    """Get system activity report"""
    try:
        db: Session = next(get_db())
        
        start_date = datetime.datetime.now(ZoneInfo("UTC")) - datetime.timedelta(days=days)
        
        # Total activities
        total_activities = db.query(ActivityLog).filter(
            ActivityLog.timestamp >= start_date
        ).count()
        
        # Activities by type
        activities_by_type = db.query(
            ActivityLog.activity_type,
            func.count(ActivityLog.id).label('count')
        ).filter(
            ActivityLog.timestamp >= start_date
        ).group_by(ActivityLog.activity_type).all()
        
        activity_breakdown = []
        for activity_type, count in activities_by_type:
            percentage = (count / total_activities * 100) if total_activities > 0 else 0
            activity_breakdown.append({
                "activity_type": activity_type.value,
                "count": count,
                "percentage": round(percentage, 2)
            })
        
        # Daily activity trend
        daily_activity = db.query(
            func.date(ActivityLog.timestamp).label('date'),
            func.count(ActivityLog.id).label('count')
        ).filter(
            ActivityLog.timestamp >= start_date
        ).group_by('date').order_by('date').all()
        
        daily_trend = []
        for date, count in daily_activity:
            daily_trend.append({
                "date": date,
                "activity_count": count
            })
        
        # Most active students
        active_students = db.query(
            ActivityLog.student_id,
            func.count(ActivityLog.id).label('activity_count')
        ).filter(
            ActivityLog.timestamp >= start_date
        ).group_by(ActivityLog.student_id).order_by(desc('activity_count')).limit(10).all()
        
        top_students = []
        for student_id, count in active_students:
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if student:
                top_students.append({
                    "student_id": student_id,
                    "student_name": student.name,
                    "activity_count": count
                })
        
        return {
            "status": "success",
            "report_period_days": days,
            "summary": {
                "total_activities": total_activities,
                "average_daily_activities": round(total_activities / days, 2) if days > 0 else 0
            },
            "activity_breakdown": activity_breakdown,
            "daily_trend": daily_trend,
            "most_active_students": top_students
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_course_performance() -> Dict[str, Any]:
    """Get course performance and completion statistics"""
    try:
        db: Session = next(get_db())
        
        # Course completion rates
        completion_stats = db.query(
            Course.course_code,
            Course.course_name,
            Course.department,
            func.count(Registration.id).label('total_registrations'),
            func.sum(case((Registration.status == 'completed', 1), else_=0)).label('completed'),
            func.avg(Registration.grade_points).label('average_grade')
        ).join(
            Registration, Course.id == Registration.course_id
        ).group_by(
            Course.id
        ).all()
        
        performance_data = []
        for course in completion_stats:
            completion_rate = (course.completed / course.total_registrations * 100) if course.total_registrations > 0 else 0
            performance_data.append({
                "course_code": course.course_code,
                "course_name": course.course_name,
                "department": course.department,
                "total_students": course.total_registrations,
                "completed": course.completed,
                "completion_rate": round(completion_rate, 2),
                "average_grade": round(course.average_grade, 2) if course.average_grade else "N/A"
            })
        
        # Department performance
        dept_performance = db.query(
            Course.department,
            func.count(Registration.id).label('total_registrations'),
            func.avg(Registration.grade_points).label('avg_grade')
        ).join(
            Registration, Course.id == Registration.course_id
        ).group_by(
            Course.department
        ).all()
        
        department_stats = []
        for dept in dept_performance:
            department_stats.append({
                "department": dept.department,
                "total_registrations": dept.total_registrations,
                "average_grade": round(dept.avg_grade, 2) if dept.avg_grade else "N/A"
            })
        
        return {
            "status": "success",
            "course_performance": performance_data,
            "department_performance": department_stats
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


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