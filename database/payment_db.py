import sqlite3

DB_PATH="data/business.db"

def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn


def save_payment(party_id,date,payment_type,amount,remarks):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        INSERT INTO payments(

            party_id,
            payment_date,
            payment_type,
            amount,
            remarks

        )

        VALUES(?,?,?,?,?)

    """,(party_id,date,payment_type,amount,remarks))

    conn.commit()
    conn.close()


def get_payments():

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        SELECT

            p.party_name,

            py.payment_date,

            py.payment_type,

            py.amount,

            py.remarks

        FROM payments py

        JOIN parties p

        ON py.party_id=p.id

        ORDER BY py.id DESC

    """)

    rows=cur.fetchall()

    conn.close()

    return rows