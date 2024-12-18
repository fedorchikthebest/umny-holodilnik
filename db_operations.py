import sqlite3
import json

con = sqlite3.connect("holodilnik.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS classes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, stop_date DATE, count INTEGER, is_kg BOOLEAN, class_id INTEGER, FOREIGN KEY (class_id)  REFERENCES classes (id))")


def get_products() -> str:
    products = cur.execute("SELECT * FROM products")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "product_name": i[1],
            "stop_date": i[2],
            "count": i[3],
            "is_kg": i[4],
            "class": class_name})
    return json.dumps(result)


def add_product(name:str, class_name:str, stop_date:str, count:int, if_kg:bool):
    if len(cur.execute("SELECT id FROM classes WHERE name = ?", (class_name,)).fetchall()) == 0:
        cur.execute("INSERT INTO classes(name) VALUES (?)", (class_name, ))
    class_id = cur.execute("SELECT id FROM classes WHERE name=?", (class_name, )).fetchall()[0][0]
    cur.execute("INSERT INTO products(name, stop_date, count, is_kg, class_id) VALUES (?, ?, ?, ?, ?)", (name, stop_date, count, if_kg, class_id))
    con.commit()
    return cur.lastrowid

