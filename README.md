\# Expense Tracker API



A FastAPI expense tracker built on top of my OOP expense tracker.



\## Run

pip install -r requirements.txt

uvicorn expense\_tracker\_api:app --reload



Then open http://127.0.0.1:8000/docs



\## Routes

\- GET /balance

\- POST /expenses

\- GET /expenses

\- DELETE /expenses/{expense\_id}

\- GET /total\_expenses

