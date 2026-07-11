import sqlite3

DB_PATH="data/business.db"

def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn


def save_purchase_return(
    bill_no,
    party_id,
    return_date,
    total
):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        INSERT INTO purchase_returns(

            bill_no,
            party_id,
            return_date,
            total

        )

        VALUES(?,?,?,?)

    """,(bill_no,party_id,return_date,total))

    conn.commit()

    return cur.lastrowid