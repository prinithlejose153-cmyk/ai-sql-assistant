import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def convert_to_sql(question: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an expert SQL generator.

Database:
Table: sales
Columns: id, customer_name, product, revenue

Rules:
- ONLY return SQL
- NO explanation
- NO text
- Only valid SQLite queries

Examples:

Q: which customer has highest revenue
A: SELECT customer_name FROM sales ORDER BY revenue DESC LIMIT 1;

Q: total revenue
A: SELECT SUM(revenue) FROM sales;

Q: which person made the most money
A: SELECT customer_name FROM sales ORDER BY revenue DESC LIMIT 1;

Now convert:

Q: {question}
A:
"""

        response = model.generate_content(prompt)

        # 🔥 SAFE EXTRACTION
        if hasattr(response, "text") and response.text:
            sql = response.text.strip()
        else:
            sql = ""

        # 🔥 CLEAN FORMATTING
        sql = sql.replace("```sql", "").replace("```", "").strip()

        # 🔥 VALIDATE OUTPUT
        if not sql or "select" not in sql.lower():
            raise ValueError("Invalid SQL generated")

        return sql

    except Exception as e:
        print("AI ERROR:", e)

        # 🔥 FALLBACK (NEVER FAIL)
        if "total" in question.lower():
            return "SELECT SUM(revenue) FROM sales;"
        elif "highest" in question.lower() or "most" in question.lower():
            return "SELECT customer_name FROM sales ORDER BY revenue DESC LIMIT 1;"
        else:
            return "SELECT * FROM sales;"