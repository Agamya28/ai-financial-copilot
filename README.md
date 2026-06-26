# AI Financial Copilot

An AI-powered personal finance assistant built with FastAPI and React.

## Features

- Transaction management
- Budget tracking
- AI financial insights
- Spending analytics dashboard
- AI chat assistant
- Financial health reports
- CSV import/export
- PDF report export

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### Frontend
- React
- Vite
- Tailwind CSS
- Recharts

## Screenshots

## Dashboard
![Dashboard Overview 1](screenshots/image-1.png)
![Dashboard Overview 2](screenshots/image-2.png)
![Dashboard Overview 3](screenshots/image-3.png)
## Transactions
![Record Daily Transactions](screenshots/image-4.png)
![Manage Daily Transactions](screenshots/image-5.png)

## Budget Management
![Budget Management](screenshots/image-6.png)

## AI Financial Report
![AI Financial Health Report- Generate personalised financial insights using AI](screenshots/image-7.png)

## AI Chat Assistant
![AI financial assistant](screenshots/image-8.png)

## Setup

### Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend

cd frontend
npm install
npm run dev

## Environment Variables

Create a `.env` file:

OPENAI_API_KEY=
DATABASE_URL=
SECRET_KEY=