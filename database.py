import sqlite3

def create_db():
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expression TEXT,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()



def save_history(expression, result):
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history(expression,result) VALUES (?,?)",
        (expression,str(result))
    )

    conn.commit()
    conn.close()

def get_history():

    conn = sqlite3.connect("calculator.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT expression,result
        FROM history
        ORDER BY id DESC
    """)

    data = cur.fetchall()

    conn.close()

    return data