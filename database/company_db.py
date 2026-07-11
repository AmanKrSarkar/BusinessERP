import sqlite3

DB_PATH = "data/business.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_company(name,address,mobile,email,gstin):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM company")

    cur.execute("""

        INSERT INTO company(

            company_name,
            address,
            mobile,
            email,
            gstin

        )

        VALUES(?,?,?,?,?)

    """,(name,address,mobile,email,gstin))

    conn.commit()
    conn.close()


def get_company():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM company LIMIT 1")

    row = cur.fetchone()

    conn.close()

    return row