
#  AI SLA Breach Prevention Platform

An intelligent AI-powered platform that predicts and prevents SLA (Service Level Agreement) violations in real-time support ticketing systems.

The system uses **LLM reasoning, vector similarity search, and hybrid risk scoring** to proactively identify high-risk tickets before they breach their SLA deadlines.

---

#  GitHub Repositories

Frontend Repository  
https://github.com/RohitChoukiker/sla-breach-prevention-agent-client.git

Backend Repository  
https://github.com/RohitChoukiker/sla-breach-prevention-agent

---

#  Project Overview

Support teams often struggle to identify tickets that may violate SLA deadlines before it is too late.

This platform introduces an **AI-driven SLA breach prevention engine** that analyzes incoming tickets using embeddings, vector search, and LLM reasoning.

Instead of reacting to breaches, the system **predicts them early and triggers preventive escalation workflows**.

Key capabilities:

• AI-based breach prediction  
• Vector similarity analysis  
• LLM reasoning for risk estimation  
• Hybrid risk scoring  
• Automated escalation workflows  

---

#  System Architecture

Frontend
• React
• TypeScript
• TailwindCSS
• ShadCN UI

Backend
• FastAPI

AI Engine
• LangGraph workflow orchestration
• Sentence Transformers embeddings

LLM
• Gemini

Vector Database
• Pinecone

Queue System
• Redis
• RQ Workers

Database
• PostgreSQL

---

#  AI Risk Prediction Engine

The core of the system is the **AI Risk Engine**, responsible for predicting SLA breach probability.

Pipeline:

Ticket Created  
↓  
Embedding Generated (SentenceTransformer)  
↓  
Vector Stored in Pinecone  
↓  
Similar Historical Tickets Retrieved  
↓  
Gemini LLM Evaluates Context  
↓  
Hybrid Risk Score Calculated  
↓  
Escalation Decision Triggered  

This hybrid approach improves accuracy by combining:

• Semantic similarity  
• Historical ticket outcomes  
• LLM contextual reasoning  

---

#  System Workflow

1. Customer creates a ticket.
2. Ticket is pushed into a Redis queue.
3. RQ worker processes the ticket asynchronously.
4. Ticket description is converted into a vector embedding.
5. Embedding is stored in Pinecone vector database.
6. Similar historical tickets are retrieved using vector search.
7. Gemini LLM analyzes ticket severity and predicts SLA breach probability.
8. Hybrid scoring algorithm calculates final risk score.
9. If risk exceeds threshold:
   - Escalation email sent
   - Ticket priority increased
   - Admin notified
10. Ticket state updated in PostgreSQL.

---

#  System Roles

Customer

• Create support tickets  
• Track ticket status  
• Monitor SLA breach risk  

Agent

• View assigned tickets  
• Update ticket status  
• Resolve support issues  

Admin

• Manage users  
• Assign agents to tickets  
• Monitor high-risk tickets  
• Override AI decisions  
• View analytics and audit logs  

---

#  Core Features

 AI-powered SLA breach prediction

 Vector similarity search with Pinecone

 Hybrid risk scoring system

 Automated escalation workflows

 Email alerts for high-risk tickets

 Admin monitoring dashboard

 Role-based authentication system

 Audit logs for administrative actions

---

#  Frontend Dashboard Modules

Customer Dashboard

• Ticket creation interface  
• Ticket monitoring  
• SLA risk visibility  

Agent Dashboard

• Assigned ticket list  
• Ticket resolution workflow  

Admin Dashboard

• System monitoring overview  
• User management  
• High-risk ticket tracking  
• Analytics and audit logs  

---

# Deployment

Frontend  
Deployed on Vercel

Backend  
Deployed on cloud server

Vector Database  
Pinecone

Queue System  
Redis + RQ Workers

Database  
PostgreSQL

---

# 🛠 Local Development Setup

Clone the repository

git clone https://github.com/your-repo-link

Navigate to project directory

cd project

Install backend dependencies

pip install -r requirements.txt

Run backend server

uvicorn main:app --reload

Install frontend dependencies

cd frontend
npm install

Run frontend

npm run dev

---

# Future Improvements

• AI-based ticket auto-classification  
• SLA breach explanation using LLM reasoning  
• Predictive analytics dashboard  
• Slack / Teams integration  
• Multi-tenant enterprise support  

---

#  Author

Rohit Choukiker

AI Engineer | Full Stack Developer

---
