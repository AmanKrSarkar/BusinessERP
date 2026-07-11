import sqlite3

from database.database import get_connection

def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn


def get_stock_ledger():

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    SELECT

        p.product_name,

        b.batch_name,

        b.expiry_date,

        b.mrp,

        b.rate,

        b.available_stock

    FROM stock_batches b

    JOIN products p

    ON b.product_id=p.id

    ORDER BY p.product_name,
             b.expiry_date

    """)

    rows=cur.fetchall()

    conn.close()

    return rows