# Hello Agent

Hello Agent is a starter full-stack application for experimenting with an
agent-powered product. The backend exposes a small FastAPI service, and the
frontend provides a Vue interface built with Vite.

## Project structure

```text
hello-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── AGENTS.md
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- Node.js `^22.18.0` or `>=24.12.0`
- npm

## Backend setup

To recreate the backend environment, run the following from the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Use `/health` for a basic
health check and `/docs` for the generated OpenAPI interface.

### Calculator API

Each calculator endpoint accepts numeric `a` and `b` query parameters and
returns a JSON object containing `result`.

| Operation | Path |
| --- | --- |
| Addition | `GET /api/calculator/add?a=8&b=2` |
| Subtraction | `GET /api/calculator/subtract?a=8&b=2` |
| Multiplication | `GET /api/calculator/multiply?a=8&b=2` |
| Division | `GET /api/calculator/divide?a=8&b=2` |

Division by zero returns HTTP `400` with
`{"detail": "Cannot divide by zero."}`.

## Frontend setup

When you are ready to install the frontend dependencies, run:

```powershell
cd frontend
npm install
npm run dev
```

The Vue application will be available at `http://localhost:5173`.

## Current status

The backend development dependencies are installed in `backend/.venv`. The
frontend dependencies are installed in `frontend/node_modules`, with ESLint
configured for code-quality checks.
