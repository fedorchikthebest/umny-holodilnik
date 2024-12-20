import sqlite3
import json

con = sqlite3.connect("holodilnik.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS classes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, stop_date DATE, count INTEGER, mass_id INTEGER, class_id INTEGER, start_date TEXT, B INTEGER, J INTEGER, U INTEGER, FOREIGN KEY (class_id)  REFERENCES classes (id))")
con.commit()
con.close()


def get_products() -> dict:
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    products = cur.execute("SELECT * FROM products")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "product_name": i[1],
            "stop_date": i[2],
            "count": i[3],
            "is_kg": i[4],
            "class": class_name,
            "start_date": i[6],
            "B": i[7],
            "J": i[8],
            "U": i[9]})
    con.close()
    return result


def add_product(name:str, class_name:str, stop_date:str, count:int, mass_id:int, start_date:str, B:int, J:int, U:int):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    if len(cur.execute("SELECT id FROM classes WHERE name = ?", (class_name,)).fetchall()) == 0:
        cur.execute("INSERT INTO classes(name) VALUES (?)", (class_name, ))
    class_id = cur.execute("SELECT id FROM classes WHERE name=?", (class_name, )).fetchall()[0][0]
    cur.execute("INSERT INTO products(name, stop_date, count, mass_id, class_id, start_date, B, J, U) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, stop_date, count, mass_id, class_id, start_date, B, J, U))
    con.commit()
    con.close()
    return cur.lastrowid


def delete_product(id: int):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    cur.execute("DELET FROM products WHERE id=?", (id,))
    con.commit()
    con.close()
