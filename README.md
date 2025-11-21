# AI University Campus Administration System

A comprehensive multi-agent university administration system built with **Google ADK** that handles student registration, course management, fee processing, analytics, and campus information through specialized AI agents.

## 🏫 System Overview

This system provides a complete AI-powered administration platform for university operations, featuring intelligent agent orchestration, database management, and specialized tools for different administrative domains.

## 🏗️ System Architecture

### **Core Components**

1. **Orchestration Agent** - Routes requests to appropriate specialized agents
2. **Registration Agent** - Manages student records and course enrollments
3. **Course Agent** - Handles course operations and scheduling
4. **Fee Agent** - Processes financial transactions and fee management
5. **Analyst Agent** - Provides analytics and data insights
6. **University Information Agent** - Offers campus and course information

### **Technology Stack**
- **Google ADK** - Agent development framework
- **Gemini 2.0 Flash** - LLM backbone
- **SQLAlchemy** - Database ORM
- **SQLite/PostgreSQL** - Database backend
- **Python** - Backend implementation

## 📁 Project Structure

```
ai_university_campus_admin_agent/
├── agent.py                          # Main orchestration agent
├── config/
│   └── database.py                   # Database models and configuration
├── agents/
│   ├── __init__.py                   # Agent exports
│   ├── registration_agent.py         # Student registration management
│   ├── course_agent.py               # Course operations
│   ├── fee_agent.py                  # Financial management
│   ├── analyst_agent.py              # Analytics and reporting
│   └── uni_information_agent.py      # Campus information
├── data/
│   ├── university_information.json   # Campus data
│   ├── course_information.json       # Course catalog
│   └── fee_information.json          # Fee structures
└── requirements.txt                  # Dependencies
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Google ADK installed
- Gemini API access

### **Installation**

1. **Clone and setup environment:**
```bash
git clone <repository>
cd ai_university_campus_admin_agent
```

2. **Install dependencies:**
```bash
pip install google-adk
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your database URL and Gemini API key
```

4. **Initialize database:**
```bash
python -c "from config.database import init_db; init_db()"
```

5. **Run the system:**
```bash
adk web
```

## 🎯 Agent Capabilities

### **Orchestration Agent**
- Intelligent request routing to specialized agents
- Multi-domain request coordination
- System-wide workflow management

### **Registration Agent**
- **Student Management**: Create, read, update, delete student records
- **Course Enrollment**: Register students for courses with capacity checks
- **Registration Tracking**: Monitor student course registrations
- **Activity Logging**: Audit trail for all student operations

**Tools Available:**
- `create_student` - Register new students
- `get_student` - Retrieve student information
- `update_student` - Modify student records
- `delete_student` - Remove student accounts
- `enroll_course` - Course registration
- `get_student_registrations` - View enrolled courses

### **Course Agent**
- **Course Catalog**: Manage course creation and updates
- **Capacity Management**: Monitor enrollment limits
- **Schedule Management**: Handle course timings and locations
- **Enrollment Tracking**: Student roster management

**Tools Available:**
- `create_course` - Add new courses to catalog
- `get_course` - Retrieve course details
- `get_all_courses` - Browse course catalog
- `update_course` - Modify course information
- `get_course_enrollments` - View class rosters
- `drop_course` - Remove students from courses

### **Fee Agent**
- **Fee Structures**: Define course-specific fee components
- **Payment Processing**: Record and track financial transactions
- **Balance Calculation**: Compute outstanding amounts
- **Financial Reporting**: Payment history and revenue tracking

**Tools Available:**
- `create_fee_structure` - Define course fees
- `get_course_fees` - View fee breakdown
- `calculate_student_fees` - Compute student balances
- `record_payment` - Process payments
- `get_payment_history` - Transaction records
- `get_fee_types` - Available fee categories

### **Analyst Agent**
- **Enrollment Analytics**: Course capacity and utilization
- **Demographic Reports**: Student population analysis
- **Financial Analytics**: Revenue and payment trends
- **Performance Metrics**: Course completion and grades
- **Activity Monitoring**: System usage statistics

**Tools Available:**
- `get_enrollment_statistics` - Course enrollment analytics
- `get_student_demographics` - Student population insights
- `get_financial_reports` - Revenue analysis
- `get_activity_report` - System usage metrics
- `get_course_performance` - Academic performance data

### **University Information Agent**
- **Campus Information**: Facilities, departments, policies
- **Course Catalog**: Detailed course descriptions and schedules
- **Fee Information**: Tuition structures and payment guidelines
- **General Queries**: Campus life and administrative procedures

## 💾 Database Schema

The system uses a comprehensive relational database with the following main tables:

- **Students** - Student personal and academic information
- **Courses** - Course catalog and scheduling
- **Registrations** - Student-course enrollment records
- **FeeStructures** - Course fee definitions
- **Payments** - Financial transaction records
- **ActivityLogs** - System audit trail
- **Departments** - Academic department information
- **AcademicRecords** - Student performance history
- **Notifications** - System communications
---

## ⚙️ Configuration

### **Environment Variables**
```env
DATABASE_URL=sqlite:///./university.db
GOOGLE_API_KEY=your_gemini_api_key
```

### **Database Support**
- **SQLite** (default) - For development and testing
- **PostgreSQL** - For production deployments
- **MySQL** - Supported via SQLAlchemy

## 🔧 Development

### **Adding New Agents**
1. Create agent file in `agents/` directory
2. Implement tools using `FunctionTool`
3. Add agent to `agents/__init__.py`
4. Register with orchestration agent in `agent.py`

### **Database Modifications**
1. Update models in `config/database.py`
2. Run database migration
3. Update relevant agent tools

## 📊 Monitoring & Analytics

The system includes comprehensive logging and analytics:
- Activity logging for all operations
- Performance metrics tracking
- Financial reporting
- Enrollment analytics
- System usage statistics

## 🔒 Security Features

- Input validation and sanitization
- SQL injection prevention via ORM
- Activity audit trails
- Data integrity constraints
- Error handling and logging

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🎓 Academic Use

This system is ideal for:
- University administration automation
- AI and multi-agent system research
- Educational technology development
- Database and system design studies

---

**Built with Google ADK and Gemini AI** - Transforming university administration through intelligent multi-agent systems.