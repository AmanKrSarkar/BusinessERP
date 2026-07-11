from database.database import get_connection

def save_adjustment(product_id,batch_id,qty,reason):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    INSERT INTO stock_adjustments(

        product_id,
        batch_id,
        qty,
        reason

    )

    VALUES(?,?,?,?)

    """,(product_id,batch_id,qty,reason))

    cur.execute("""

    UPDATE stock_batches

    SET available_stock=available_stock+?

    WHERE id=?

    """,(qty,batch_id))

    conn.commit()
    conn.close()