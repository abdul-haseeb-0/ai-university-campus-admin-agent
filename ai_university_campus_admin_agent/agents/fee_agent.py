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

load_dotenv()

# ===============================================================================
# Fee Management Tools

def create_fee_structure(course_code: str, fee_type: str, amount: float, 
                        description: Optional[str] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
    """Create a new fee structure for a course"""
    try:
        db: Session = next(get_db())
        
        # Check if course exists
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        # Validate fee type
        try:
            fee_type_enum = FeeType(fee_type.lower())
        except ValueError:
            valid_types = [t.value for t in FeeType]
            return {"status": "error", "message": f"Invalid fee type. Valid types: {', '.join(valid_types)}"}
        
        # Parse due date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {"status": "error", "message": "Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}
        
        new_fee_structure = FeeStructure(
            course_id=course.id,
            fee_type=fee_type_enum,
            amount=amount,
            description=description,
            due_date=due_date_obj,
            is_active=True,
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        
        db.add(new_fee_structure)
        db.commit()
        db.refresh(new_fee_structure)
        
        return {
            "status": "success",
            "message": "Fee structure created successfully",
            "fee_structure": {
                "id": new_fee_structure.id,
                "course_code": course_code,
                "fee_type": new_fee_structure.fee_type.value,
                "amount": new_fee_structure.amount,
                "description": new_fee_structure.description,
                "due_date": new_fee_structure.due_date.isoformat() if new_fee_structure.due_date else None
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_course_fees(course_code: str) -> Dict[str, Any]:
    """Get all fee structures for a course"""
    try:
        db: Session = next(get_db())
        
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        fees = db.query(FeeStructure).filter(
            FeeStructure.course_id == course.id,
            FeeStructure.is_active == True
        ).all()
        
        total_amount = sum(fee.amount for fee in fees)
        
        result = []
        for fee in fees:
            result.append({
                "fee_type": fee.fee_type.value,
                "amount": fee.amount,
                "description": fee.description,
                "due_date": fee.due_date.isoformat() if fee.due_date else None
            })
        
        return {
            "status": "success",
            "course_code": course_code,
            "course_name": course.course_name,
            "fees": result,
            "total_amount": total_amount,
            "currency": "USD"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def calculate_student_fees(student_id: str, course_code: str) -> Dict[str, Any]:
    """Calculate total fees for a student for a specific course"""
    try:
        db: Session = next(get_db())
        
        # Check if student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        # Check if course exists
        course = db.query(Course).filter(Course.course_code == course_code).first()
        if not course:
            return {"status": "error", "message": "Course not found"}
        
        # Get active fees for the course
        fees = db.query(FeeStructure).filter(
            FeeStructure.course_id == course.id,
            FeeStructure.is_active == True
        ).all()
        
        # Get payments made by student for this course
        payments = db.query(Payment).filter(
            Payment.student_id == student_id,
            Payment.fee_structure_id.in_([fee.id for fee in fees])
        ).all()
        
        total_fees = sum(fee.amount for fee in fees)
        total_paid = sum(payment.amount_paid for payment in payments)
        balance_due = total_fees - total_paid
        
        fee_breakdown = []
        for fee in fees:
            fee_paid = sum(p.amount_paid for p in payments if p.fee_structure_id == fee.id)
            fee_balance = fee.amount - fee_paid
            
            fee_breakdown.append({
                "fee_type": fee.fee_type.value,
                "amount": fee.amount,
                "paid": fee_paid,
                "balance": fee_balance,
                "description": fee.description,
                "due_date": fee.due_date.isoformat() if fee.due_date else None
            })
        
        return {
            "status": "success",
            "student_id": student_id,
            "student_name": student.name,
            "course_code": course_code,
            "course_name": course.course_name,
            "fee_breakdown": fee_breakdown,
            "summary": {
                "total_fees": total_fees,
                "total_paid": total_paid,
                "balance_due": balance_due,
                "currency": "USD"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def record_payment(student_id: str, amount: float, payment_method: str, 
                  course_code: Optional[str] = None, fee_type: Optional[str] = None,
                  transaction_id: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
    """Record a payment made by a student"""
    try:
        db: Session = next(get_db())
        
        # Check if student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        # Validate payment method
        valid_methods = ["credit_card", "bank_transfer", "cash", "check", "online"]
        if payment_method not in valid_methods:
            return {"status": "error", "message": f"Invalid payment method. Valid methods: {', '.join(valid_methods)}"}
        
        # Find fee structure if course and fee type specified
        fee_structure_id = None
        if course_code and fee_type:
            course = db.query(Course).filter(Course.course_code == course_code).first()
            if not course:
                return {"status": "error", "message": "Course not found"}
            
            try:
                fee_type_enum = FeeType(fee_type.lower())
            except ValueError:
                valid_types = [t.value for t in FeeType]
                return {"status": "error", "message": f"Invalid fee type. Valid types: {', '.join(valid_types)}"}
            
            fee_structure = db.query(FeeStructure).filter(
                FeeStructure.course_id == course.id,
                FeeStructure.fee_type == fee_type_enum,
                FeeStructure.is_active == True
            ).first()
            
            if not fee_structure:
                return {"status": "error", "message": f"No active fee structure found for {fee_type} in {course_code}"}
            
            fee_structure_id = fee_structure.id
        
        # Generate transaction ID if not provided
        if not transaction_id:
            transaction_id = f"TXN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{student_id[-4:]}"
        
        # Check if transaction ID already exists
        existing_txn = db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
        if existing_txn:
            return {"status": "error", "message": "Transaction ID already exists"}
        
        new_payment = Payment(
            student_id=student_id,
            fee_structure_id=fee_structure_id,
            amount_paid=amount,
            payment_date=datetime.datetime.now(ZoneInfo("UTC")),
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=PaymentStatus.PAID,
            notes=notes,
            created_at=datetime.datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.datetime.now(ZoneInfo("UTC"))
        )
        
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        
        return {
            "status": "success",
            "message": "Payment recorded successfully",
            "payment": {
                "transaction_id": new_payment.transaction_id,
                "student_id": new_payment.student_id,
                "amount": new_payment.amount_paid,
                "payment_method": new_payment.payment_method,
                "payment_date": new_payment.payment_date.isoformat(),
                "status": new_payment.status.value
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_payment_history(student_id: str, course_code: Optional[str] = None) -> Dict[str, Any]:
    """Get payment history for a student"""
    try:
        db: Session = next(get_db())
        
        # Check if student exists
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        query = db.query(Payment, FeeStructure, Course).join(
            FeeStructure, Payment.fee_structure_id == FeeStructure.id, isouter=True
        ).join(
            Course, FeeStructure.course_id == Course.id, isouter=True
        ).filter(Payment.student_id == student_id)
        
        if course_code:
            course = db.query(Course).filter(Course.course_code == course_code).first()
            if course:
                query = query.filter(FeeStructure.course_id == course.id)
        
        payments = query.order_by(Payment.payment_date.desc()).all()
        
        result = []
        total_paid = 0
        
        for payment, fee_structure, course in payments:
            result.append({
                "transaction_id": payment.transaction_id,
                "amount": payment.amount_paid,
                "payment_method": payment.payment_method,
                "payment_date": payment.payment_date.isoformat(),
                "status": payment.status.value,
                "course_code": course.course_code if course else "General",
                "fee_type": fee_structure.fee_type.value if fee_structure else "General",
                "notes": payment.notes
            })
            total_paid += payment.amount_paid
        
        return {
            "status": "success",
            "student_id": student_id,
            "student_name": student.name,
            "payments": result,
            "total_payments": len(result),
            "total_amount_paid": total_paid,
            "currency": "USD"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_fee_types() -> Dict[str, Any]:
    """Get all available fee types"""
    try:
        fee_types = [fee_type.value for fee_type in FeeType]
        
        return {
            "status": "success",
            "fee_types": fee_types,
            "count": len(fee_types)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

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