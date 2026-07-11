import sqlite3

DB_PATH = "data/business.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_parties():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            id,
            party_name,
            mobile,
            gstin,
            address

        FROM parties

        ORDER BY party_name

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def update_party(pid,name,mobile,gstin,address):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE parties

        SET

            party_name=?,
            mobile=?,
            gstin=?,
            address=?

        WHERE id=?

    """,(name,mobile,gstin,address,pid))

    conn.commit()
    conn.close()


def delete_party(pid):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM parties WHERE id=?",
        (pid,)
    )

    conn.commit()
    conn.close()