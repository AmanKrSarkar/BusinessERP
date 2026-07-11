import sqlite3

from database.database import get_connection

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_party_ledger():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            p.party_name,

            s.invoice_number,

            s.invoice_date,

            s.net_amount

        FROM sales_bills s

        JOIN parties p
        ON s.party_id=p.id

        ORDER BY s.invoice_date DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows