from database.database import get_connection


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