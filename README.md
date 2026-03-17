# AI SLA Breach Prevention Platform

An AI-powered SLA breach prediction platform that proactively identifies support tickets at risk of violating Service Level Agreements (SLA).

The system combines LLM reasoning, semantic vector search, and machine learning risk scoring to detect potential SLA breaches early and trigger preventive escalation workflows.

Instead of reacting to SLA violations after they occur, this platform predicts them before they happen.

---

# Live Demo
 
https://sla-breach-prevention-agent-client.vercel.app

---

# GitHub Repositories

Frontend Repository  
https://github.com/RohitChoukiker/sla-breach-prevention-agent-client

Backend Repository  
https://github.com/RohitChoukiker/sla-breach-prevention-agent

---

# Project Overview

Support teams often struggle to identify which tickets are likely to violate SLA deadlines before it is too late.

This platform introduces an AI-driven SLA breach prevention engine that analyzes incoming tickets using:

- Semantic embeddings
- Vector similarity search
- Large Language Model reasoning
- Hybrid risk scoring

The system continuously evaluates ticket risk and triggers proactive escalation workflows.

---

# System Architecture

Frontend

- React
- TypeScript
- TailwindCSS
- ShadCN UI

Backend

- FastAPI

AI Engine

- LangGraph workflow orchestration
- SentenceTransformers embeddings
- Custom ML prediction model

LLM

- Gemini

Vector Database

- Pinecone

Queue System

- Redis
- RQ Workers

Database

- PostgreSQL

---

# AI Risk Prediction Engine

The AI Risk Engine predicts the probability of SLA breach for each ticket.

Pipeline

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
Machine Learning Model Prediction  
↓  
Hybrid Risk Score Calculation  
↓  
Escalation Decision Triggered  

This hybrid approach combines:

- Semantic similarity
- Historical ticket outcomes
- Machine learning prediction
- LLM contextual reasoning

---

# System Workflow

1. Customer creates a ticket.
2. Ticket is pushed into a Redis queue.
3. RQ worker processes the ticket asynchronously.
4. Ticket description is converted into a vector embedding.
5. Embedding is stored in Pinecone.
6. Similar historical tickets are retrieved using vector search.
7. Gemini LLM analyzes ticket severity.
8. ML model predicts breach probability.
9. Hybrid scoring calculates final risk score.
10. If risk exceeds threshold:
   - Escalation email sent
   - Ticket priority increased
   - Admin notified
11. Ticket state updated in PostgreSQL.

---

# User Roles

Customer

- Create support tickets
- Track ticket status
- Monitor SLA breach risk

Agent

- View assigned tickets
- Update ticket status
- Resolve issues

Admin

- Manage users
- Assign agents
- Monitor high-risk tickets
- Override AI decisions
- View analytics and audit logs

---

# Core Features

- AI-powered SLA breach prediction
- Vector similarity search using Pinecone
- Hybrid ML + rule-based risk scoring
- Automated escalation workflows
- Email alerts for high-risk tickets
- Admin monitoring dashboard
- Role-based authentication
- Audit logging

---

# Frontend Dashboard Modules

Customer Dashboard

- Ticket creation
- Ticket monitoring
- SLA risk visibility

Agent Dashboard

- Assigned ticket list
- Ticket resolution workflow

Admin Dashboard

- System monitoring overview
- User management
- High-risk ticket tracking
- Analytics and audit logs

---

# Deployment

Frontend

Deployed on Vercel

Backend

FastAPI deployed on cloud server

Vector Database

Pinecone

Queue System

Redis + RQ Workers

Database

PostgreSQL

---

# Local Development Setup

Clone repository

git clone https://github.com/RohitChoukiker/sla-breach-prevention-agent

Navigate to project

cd sla-breach-prevention-agent

Install backend dependencies

pip install -r requirements.txt

Run backend

uvicorn main:app --reload

Run worker

python task_queue/worker.py

Frontend setup

cd frontend  
npm install  
npm run dev

---

# Future Improvements

- AI-based ticket auto-classification
- Explainable SLA risk predictions
- Predictive analytics dashboard
- Multi-tenant enterprise support

---

# Author

Rohit Choukiker

AI Engineer | Full Stack Developer

GitHub  
https://github.com/RohitChoukiker

---

# License

MIT License

EOF
