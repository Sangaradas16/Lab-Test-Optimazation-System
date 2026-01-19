$BackendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\venv\Scripts\activate; uvicorn main:app --reload --port 8000" -PassThru
$FrontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -PassThru

Write-Host "Lab Test Optimization System Started."
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"
