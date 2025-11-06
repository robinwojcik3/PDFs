@echo off
REM Script de démarrage pour PDF Explorer (Windows)

echo Starting PDF Explorer...
echo.

REM Démarrer le backend
echo Starting Backend...
start "PDF Explorer Backend" cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Attendre 5 secondes
timeout /t 5 /nobreak

REM Démarrer le frontend
echo Starting Frontend...
start "PDF Explorer Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Application started!
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000/docs
echo.
echo Press any key to stop the services...
pause

REM Arrêter les services
taskkill /FI "WindowTitle eq PDF Explorer Backend*" /T /F
taskkill /FI "WindowTitle eq PDF Explorer Frontend*" /T /F
