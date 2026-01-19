# Lab Test Optimization System

A Next.js frontend and FastAPI backend application for optimizing lab test recommendations.

## Prerequisites

-   Node.js & npm
-   Python 3.8+
-   PowerShell (for start script)

## Quick Start (Recommended)

The easiest way to run the application is using the provided PowerShell script:

```powershell
.\start_app.ps1
```

This will automatically:
1.  Start the Backend server on `http://localhost:8000`
2.  Start the Frontend development server on `http://localhost:3000`

## Manual Startup

If you prefer to run services manually or encounter issues with the script:

### 1. Start Backend

Open a terminal in the project root:

```powershell
cd backend
# Create/Activate virtual environment if needed
# python -m venv venv
..\venv\Scripts\activate
# Install requirements if needed
# pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend

Open a second terminal in the project root:

```powershell
cd frontend
# Install dependencies if needed
# npm install
npm run dev
```

## Access

-   **Frontend**: [http://localhost:3000](http://localhost:3000)
-   **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
