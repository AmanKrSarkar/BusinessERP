import sqlite3

DB_PATH = "data/business.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_current_stock():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT

            p.product_name,
            p.company,
            b.batch_name,
            b.expiry_date,
            b.mrp,
            b.rate,
            b.available_stock

        FROM stock_batches b

        JOIN products p
        ON b.product_id = p.id

        WHERE b.available_stock > 0

        ORDER BY p.product_name,
                 b.expiry_date
    """)

    rows = cur.fetchall()

    conn.close()

    return rows