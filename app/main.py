from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
import sqlite3
import os

from app.services.nl_to_sql import convert_to_sql

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
)

# ✅ DB PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "sales.db")


# ✅ FUNCTION: RUN SQL QUERY
def run_query(query: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        conn.close()
        return result

    except Exception as e:
        return f"DB Error: {str(e)}"


# ✅ HOME ROUTE
@app.get("/")
def home():
    return {"message": "AI SQL Assistant is running 🚀"}


# ✅ MAIN AI ENDPOINT
@app.get("/ask")
def ask(q: str = Query(...)):
    try:
        sql = convert_to_sql(q)

        # 🔥 Handle AI failure
        if not sql or not isinstance(sql, str):
            return {
                "question": q,
                "sql": None,
                "result": "AI failed to generate SQL. Try rephrasing."
            }

        result = run_query(sql)

        return {
            "question": q,
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {
            "question": q,
            "sql": None,
            "result": f"Server Error: {str(e)}"
        }


# ✅ DEBUG ENDPOINT (TEST DB DIRECTLY)
@app.get("/test-db")
def test_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales")
        result = cursor.fetchall()

        conn.close()

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }