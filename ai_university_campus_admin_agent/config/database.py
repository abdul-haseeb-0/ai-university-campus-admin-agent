from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, CheckConstraint, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
from datetime import datetime
import enum

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# For SQLite, add connection args
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums for better data integrity
class ActivityType(enum.Enum):
    LOGIN = "login"
    PROFILE_UPDATE = "profile_update"
    COURSE_REGISTRATION = "course_registration"
    COURSE_DROP = "course_drop"
    PAYMENT = "payment"
    EMAIL_SENT = "email_sent"
    SYSTEM_ACTION = "system_action"

class RegistrationStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DROPPED = "dropped"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"

class FeeType(enum.Enum):
    TUITION = "tuition"
    LAB_FEE = "lab_fee"
    LIBRARY_FEE = "library_fee"
    TECHNOLOGY_FEE = "technology_fee"
    REGISTRATION_FEE = "registration_fee"
    EXAM_FEE = "exam_fee"
    OTHER = "other"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    REFUNDED = "refunded"

# Database Models
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    date_of_birth = Column(DateTime)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    graduation_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="student", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="student", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="student", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('email LIKE "%@%"', name='valid_email'),
    )

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    description = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="activity_logs")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, index=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    description = Column(Text)
    credits = Column(Integer, nullable=False)
    department = Column(String(100), nullable=False)
    semester = Column(String(20))  # Fall, Spring, Summer
    year = Column(Integer)
    max_capacity = Column(Integer, default=30)
    current_enrollment = Column(Integer, default=0)
    instructor = Column(String(100))
    schedule = Column(String(100))  # "MWF 9:00-10:00"
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    prerequisites = Column(Text)  # JSON string or comma-separated course codes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fee_structures = relationship("FeeStructure", back_populates="course", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="course", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('credits > 0', name='positive_credits'),
        CheckConstraint('max_capacity >= current_enrollment', name='capacity_check'),
    )

class FeeStructure(Base):
    __tablename__ = "fee_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="fee_structures")
    payments = relationship("Payment", back_populates="fee_structure")
    
    __table_args__ = (
        CheckConstraint('amount >= 0', name='non_negative_amount'),
    )

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING)
    grade = Column(String(5))  # A, B+, C, etc.
    grade_points = Column(Float)
    completion_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="registrations")
    course = relationship("Course", back_populates="registrations")
    payments = relationship("Payment", back_populates="registration")
    
    __table_args__ = (
        CheckConstraint('grade_points >= 0 AND grade_points <= 4.0', name='valid_grade_points'),
    )

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    registration_id = Column(Integer, ForeignKey('registrations.id'))
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'))
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50))  # credit_card, bank_transfer, cash, etc.
    transaction_id = Column(String(100), unique=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="payments")
    registration = relationship("Registration", back_populates="payments")
    fee_structure = relationship("FeeStructure", back_populates="payments")
    
    __table_args__ = (
        CheckConstraint('amount_paid > 0', name='positive_payment'),
    )

# Additional tables for enhanced functionality
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(10), unique=True, nullable=False)
    department_name = Column(String(100), nullable=False)
    head_of_department = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AcademicRecord(Base):
    __tablename__ = "academic_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'), nullable=False)
    semester = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    total_credits = Column(Integer, default=0)
    gpa = Column(Float, default=0.0)
    standing = Column(String(50))  # Freshman, Sophomore, Junior, Senior
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")
    
    __table_args__ = (
        CheckConstraint('gpa >= 0 AND gpa <= 4.0', name='valid_gpa_range'),
        CheckConstraint('total_credits >= 0', name='non_negative_credits'),
    )

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey('students.student_id'))
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))  # academic, financial, system, etc.
    is_read = Column(Boolean, default=False)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    sent_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database and create all tables"""
    try:
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Test connection
        with engine.connect() as connection:
            print("✅ Database connection successful.")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()

# Test database connection and initialization
if __name__ == "__main__":
    init_db()