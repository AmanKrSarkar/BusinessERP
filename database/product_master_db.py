import sqlite3

DB_PATH = "data/business.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_products():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            id,
            product_name,
            company,
            hsn_code,
            gst_percent

        FROM products

        ORDER BY product_name

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def update_product(pid,name,company,hsn,gst):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE products

        SET

            product_name=?,
            company=?,
            hsn_code=?,
            gst_percent=?

        WHERE id=?

    """,(name,company,hsn,gst,pid))

    conn.commit()
    conn.close()


def delete_product(pid):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(

        "DELETE FROM products WHERE id=?",

        (pid,)

    )

    conn.commit()
    conn.close()