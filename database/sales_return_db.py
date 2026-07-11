import sqlite3

from database.database import get_connection

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_sales_return(invoice_no, party_id, return_date, total):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO sales_returns(

            invoice_no,
            party_id,
            return_date,
            total

        )

        VALUES(?,?,?,?)

    """,(invoice_no,party_id,return_date,total))

    conn.commit()

    return cur.lastrowid