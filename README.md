AI Job Dashboard

A full-stack AI web application that analyzes job datasets, recommends suitable roles, and matches resumes using AI. Includes interactive charts for job categories, top skills, and resume-job matching. Built with FastAPI (backend) and HTML/JS + Chart.js (frontend).

Features

CSV Upload & Preview: Upload job datasets and view rows, columns, and sample data.

Job Analysis: Detect top skills and categorize jobs (AI/Data Science, Web Dev, DevOps, etc.).

Role Recommendations: Suggests suitable roles based on job description keywords.

Resume Matching: Upload a resume and match top 5 jobs from the dataset using AI (cosine similarity).

Interactive Charts: Visualize job categories and recommended roles dynamically with Chart.js.

Deployment Ready: Can be deployed as a web application with a public link.

Tech Stack

Backend: FastAPI, Pandas, Scikit-learn

Frontend: HTML, CSS, JavaScript, Chart.js

Deployment: Render / Ngrok

Folder Structure
AI-Job-Dashboard/
│
├── app.py               # Backend FastAPI app
├── requirements.txt     # Python dependencies
├── frontend/            # Frontend HTML + JS + CSS
└── backend/             # Additional Python modules (optional)

Local Setup

Clone or download the repo.

Create a virtual environment:

python -m venv venv


Activate virtual environment:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt


Run backend:

uvicorn app:app --reload


Run frontend:

cd frontend
python -m http.server 5500


Open browser:

http://localhost:5500

Usage

Upload job CSV file.

Analyze jobs → see top skills & job categories chart.

Recommend roles → see suggested roles chart.

Upload resume → match top 5 jobs from your dataset.

Deployment

Render: Push project to GitHub (or use ngrok for local public URL)

Update frontend API variable with deployed backend URL:

const API = "https://your-backend-url.com";


Frontend + backend works as a fully interactive dashboard.

Screenshots / Demo

(Optional: add screenshots of your charts, resume match, and dashboard)


Author

Rabia Sarwar – Full-stack AI Developer | UI/UX Enthusiast | Portfolio-ready AI Projects
