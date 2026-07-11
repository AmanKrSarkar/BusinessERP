import sqlite3

DB_PATH = "data/business.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_payment_register():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            py.id,
            p.party_name,
            py.payment_date,
            py.payment_type,
            py.amount,
            py.remarks

        FROM payments py

        LEFT JOIN parties p
        ON py.party_id=p.id

        ORDER BY py.id DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows