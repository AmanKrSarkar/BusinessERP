from database.database import get_connection


def get_sales_register():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            s.id,
            s.invoice_number,
            s.invoice_date,
            p.party_name,
            s.net_amount

        FROM sales_bills s

        LEFT JOIN parties p
        ON s.party_id=p.id

        ORDER BY s.id DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows