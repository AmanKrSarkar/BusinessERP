import sqlite3

DB_PATH = "data/business.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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