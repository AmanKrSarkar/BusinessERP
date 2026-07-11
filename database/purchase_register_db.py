import sqlite3

from database.database import get_connection

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_purchase_register():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            pb.id,
            pb.invoice_number,
            pb.invoice_date,
            p.party_name,
            pb.net_amount

        FROM purchase_bills pb

        LEFT JOIN parties p
        ON pb.party_id = p.id

        ORDER BY pb.id DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows