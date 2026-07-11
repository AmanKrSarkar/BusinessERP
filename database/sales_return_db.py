from database.database import get_connection


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