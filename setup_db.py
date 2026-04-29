import sqlite3

conn = sqlite3.connect("app/data/sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    product TEXT,
    revenue INTEGER
)
""")

data = [
    ("John", "Laptop", 80000),
    ("Alice", "Phone", 50000),
    ("Bob", "Tablet", 30000),
    ("John", "Phone", 40000),
    ("Alice", "Laptop", 90000)
]

cursor.executemany(
    "INSERT INTO sales (customer_name, product, revenue) VALUES (?, ?, ?)",
    data
)

conn.commit()
conn.close()

print("Database created successfully!")