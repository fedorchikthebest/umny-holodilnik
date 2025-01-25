import sqlite3
import json
import datetime

con = sqlite3.connect("holodilnik.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS classes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, stop_date TEXT, count INTEGER, mass_id INTEGER, class_id INTEGER, start_date TEXT, B INTEGER, J INTEGER, U INTEGER, is_deleted BOOL, delete_time INTEGER, create_time INTEGER, FOREIGN KEY (class_id)  REFERENCES classes (id))")
cur.execute("CREATE TABLE IF NOT EXISTS buys(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, FOREIGN KEY (product_id)  REFERENCES products (id), UNIQUE (product_id))")
con.commit()
con.close()


def get_products() -> list:
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    products = cur.execute("SELECT * FROM products WHERE is_deleted=0")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "id": i[0],
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
    cur.execute(f"INSERT INTO products(name, stop_date, count, mass_id, class_id, start_date, B, J, U, is_deleted, create_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, {datetime.datetime.now().strftime('%s')})", (name, stop_date, count, mass_id, class_id, start_date, B, J, U))
    con.commit()
    con.close()
    return cur.lastrowid


def delete_product(id: int):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    cur.execute(f"UPDATE products SET is_deleted=1, delete_time={datetime.datetime.now().strftime('%s')} WHERE id = ?", (id,))
    con.commit()
    con.close()


def get_product(id_: int, r_id=None):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    r_id = id_ if r_id is None else r_id

    products = cur.execute("SELECT * FROM products WHERE id == ?", (id_,)).fetchone()
    class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (products[5],)).fetchone()[0]
    con.close()
    return {
        'id': r_id,
        "product_name": products[1],
        "stop_date": products[2],
        "count": products[3],
        "is_kg": products[4],
        "class": class_name,
        "start_date": products[6],
        "B": products[7],
        "J": products[8],
        "U": products[9]}


def add_buy(id_):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO buys(product_id) VALUES (?)", (id_,))
    except Exception:
        pass
    con.commit()
    con.close()


def get_buy(id_):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    a = get_product(cur.execute("SELECT * FROM buys WHERE product_id=?", (id_, )).fetchone()[0])
    con.close()
    return a


def get_buys():
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()
    
    a = map(lambda x: get_product(x[1], x[0]), cur.execute("SELECT * FROM buys").fetchall())
    con.close()
    return list(a)


def delete_buy(id_):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()
    
    cur.execute("DELETE FROM buys WHERE id=?", (id_,))
    con.commit()
    con.close()


def get_deleted():
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    products = cur.execute("SELECT * FROM products WHERE is_deleted=1")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "id": i[0],
            "product_name": i[1],
            "stop_date": i[2],
            "count": i[3],
            "is_kg": i[4],
            "class": class_name,
            "start_date": i[6],
            "B": i[7],
            "J": i[8],
            "U": i[9],
            "delete_date": i[11]})
    con.close()
    return result


def get_products_stamp(start: int, stop: int):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    products = cur.execute(f"SELECT * FROM products WHERE is_deleted=0 AND create_time >= {start} AND create_time <= {stop}")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "id": i[0],
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

def get_deleted_stamp(start: int, stop: int):
    con = sqlite3.connect("holodilnik.db")
    cur = con.cursor()

    products = cur.execute(f"SELECT * FROM products WHERE is_deleted=1 AND create_time >= {start} AND create_time <= {stop}")
    result = []
    for i in products.fetchall():
        class_name = cur.execute("SELECT name FROM classes WHERE id == ?", (i[5],)).fetchone()[0]
        result.append({
            "id": i[0],
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


