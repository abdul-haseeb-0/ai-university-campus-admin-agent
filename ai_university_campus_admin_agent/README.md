# University Assistant System (Google ADK Implementation)

A modular, multi-agent university-assistant platform built using **Google ADK**.  
The system uses ADK's orchestration, routing, tools, and memory capabilities to manage information about courses, fees, campus, analytics, and more.

---

## 📌 System Architecture Overview

### **1. Orchestration Agent**
Central agent responsible for:
- Routing queries to the correct specialist agent
- Maintaining workflow logic
- Executing multi-step tasks
- Coordinating tool usage and memory exposure across the system

### **2. Registration Agent (CRUD Tools)**
Handles:
- Student registration
- Student records management (Create, Read, Update, Delete)
- Course enrollment and dropping
- Profile management via ADK Tool functions

### **3. Campus Information Agent (RAG)**
Retrieves factual content from a university knowledge base using RAG:
- Campus departments  
- Facilities  
- Maps  
- Policies  
- Contacts  

### **4. Analyst Agent**
Performs analytical operations:
- Statistical analysis  
- Academic risk prediction  
- Performance summaries  
- Trends and insights for courses or departments  
- Uses ADK tool functions for computations

### **5. Course Information Agent (RAG)**
Retrieves structured course information:
- Course timings  
- Class schedules  
- Faculty information  
- Course outlines  
- Weekly lesson plans  

### **6. Fee Agent (RAG)**
Handles:
- Fee structure queries  
- Payment schedules  
- Instalment plans  
- Scholarship requirements  
- Late-fee rules  

### **7. Advisor Agent**
Provides personalized study suggestions:
- Based on completed courses  
- Program requirements  
- Available courses  
- Career alignment  
- Academic performance trends  

---

## 🧩 Features

- Modular multi-agent setup using ADK
- Routing and orchestration handled by an Orchestration Agent
- CRUD-enabled Registration Agent
- 3 RAG-powered knowledge agents:
  - Campus Information
  - Course Information
  - Fee Information
- Analytical processing with the Analyst Agent
- Personalized academic guidance through Advisor Agent
- Full ADK environment compatibility using `adk run`
- Extensible tools for data access, analytics, and retrieval

---

## 📁 Project Structure

```

project-root/
│
├── models.py
├── main.py
├── tools/
│   ├── registration_tools.py
│   ├── analysis_tools.py
│   ├── rag_tools.py
│   └── advisor_tools.py
│
├── data/
│   ├── campus_knowledgebase/
│   ├── course_data/
│   └── fee_data/
│
└── README.md

```

---

## 🚀 Getting Started

### **1. Install Dependencies**
```

pip install -r requirements.txt

```

### **2. Run with Google ADK**
```

adk run

```

### **3. Configure Environment**
Set environment variables:
```

export ADK_ENV=production

```

---

## 🛠 Tools Overview

### **Registration Tools (CRUD)**
- `create_student()`
- `get_student()`
- `update_student()`
- `delete_student()`
- `enroll_course()`
- `drop_course()`

### **RAG Tools**
- `retrieve_campus_info()`
- `retrieve_course_info()`
- `retrieve_fee_info()`

### **Analyst Tools**
- `calculate_gpa()`
- `predict_risk()`
- `summarize_performance()`
- `run_statistical_analysis()`

### **Advisor Tools**
- `advise_next_course()`
- `map_degree_path()`

---

## 🧠 Agent Orchestration

The Orchestration Agent:
- Reads user message
- Detects intent using ADK's model
- Routes task to correct agent:
  - Registration
  - Campus
  - Course
  - Fee
  - Analyst
  - Advisor
- Executes multi-step plans
- Returns combined structured output

---

## 🧪 Example Query Flows

### **1. “Register me for AI-501”**
Flow:
1. Orchestration Agent → detect intent  
2. Registration Agent → check student status  
3. Registration Agent → enroll course  
4. Return success response  

### **2. “What are the timings of CS-220?”**
Flow:
1. Orchestration Agent  
2. Course Information Agent (RAG)  
3. RAG retrieves schedule  
4. Answer returned  

### **3. “Advise me which subject I should take next semester”**
Flow:
1. Orchestration  
2. Analyst Agent to load performance  
3. Advisor Agent to suggest course path  
4. Final result merged  

---

## 📌 Future Enhancements

- Add vector memory for personalized long-term advising
- Connect to real university API database
- Add dashboards for analytics agent
- Integrate user authentication and multi-session memory

---

## ✔️ License
This project is open and customizable for educational and institutional use.

```