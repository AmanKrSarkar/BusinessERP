from database.database import get_connection


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