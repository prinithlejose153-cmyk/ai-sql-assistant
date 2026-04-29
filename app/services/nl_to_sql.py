import re

def convert_to_sql(question: str) -> str:
    q = question.lower()

    # 🔥 remove punctuation
    q = re.sub(r"[^\w\s]", "", q)

    # 💡 INTENT DETECTION

    # 1. Highest revenue
    if any(word in q for word in ["highest", "top", "most", "max"]):
        if any(word in q for word in ["customer", "person", "who"]):
            return "SELECT customer_name FROM sales ORDER BY revenue DESC LIMIT 1;"

    # 2. Total revenue
    if "total" in q or "sum" in q:
        return "SELECT SUM(revenue) FROM sales;"

    # 3. Show all data
    if any(word in q for word in ["all", "show", "list"]):
        return "SELECT * FROM sales;"

    # 4. Revenue by customer
    if "revenue" in q and "customer" in q:
        return "SELECT customer_name, SUM(revenue) FROM sales GROUP BY customer_name;"

    # 5. Product queries
    if "product" in q:
        return "SELECT * FROM sales;"

    # ❌ fallback
    return None