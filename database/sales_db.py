import sqlite3

DB_PATH = "data/business.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# CREATE SALES BILL
# ==========================================

def create_sales_bill(
    invoice_number,
    invoice_date,
    party_id,
    gross,
    other,
    roundoff,
    net
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sales_bills
        (
            invoice_number,
            invoice_date,
            party_id,
            gross_amount,
            other_charges,
            round_off,
            net_amount
        )
        VALUES
        (
            ?,?,?,?,?,?,?
        )
    """,(
        invoice_number,
        invoice_date,
        party_id,
        gross,
        other,
        roundoff,
        net
    ))

    bill_id = cur.lastrowid

    conn.commit()
    conn.close()

    return bill_id


# ==========================================
# SAVE SALES ITEM
# ==========================================

def save_sales_item(
    bill_id,
    product_id,
    batch_id,
    qty,
    rate,
    disc1,
    disc2,
    gst,
    taxable,
    total
):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
        INSERT INTO sales_items
        (
            sales_bill_id,
            product_id,
            batch_id,
            qty,
            rate,
            disc1,
            disc2,
            gst,
            taxable,
            total
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?
        )
    """,(
        bill_id,
        product_id,
        batch_id,
        qty,
        rate,
        disc1,
        disc2,
        gst,
        taxable,
        total
    ))

    conn.commit()
    conn.close()


# ==========================================
# FIFO
# ==========================================

def get_fifo_batches(product_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *

        FROM stock_batches

        WHERE product_id=?
        AND available_stock>0

        ORDER BY expiry_date ASC,id ASC
    """,(product_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

def fifo_sale(product_id, sale_qty):

    batches = get_fifo_batches(product_id)

    used_batches = []

    remaining = sale_qty

    conn = get_connection()
    cur = conn.cursor()

    for batch in batches:

        if remaining <= 0:
            break

        stock = batch["available_stock"]

        if stock >= remaining:

            cur.execute("""

                UPDATE stock_batches

                SET available_stock=available_stock-?

                WHERE id=?

            """,(remaining,batch["id"]))

            used_batches.append((batch["id"],remaining))

            remaining = 0

        else:

            cur.execute("""

                UPDATE stock_batches

                SET available_stock=0

                WHERE id=?

            """,(batch["id"],))

            used_batches.append((batch["id"],stock))

            remaining -= stock

    conn.commit()
    conn.close()

    return used_batches,remaining


# ==========================================
# REDUCE STOCK
# ==========================================

def reduce_stock(batch_id,qty):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        UPDATE stock_batches

        SET available_stock=
        available_stock-?

        WHERE id=?

    """,(qty,batch_id))

    conn.commit()
    conn.close()

def get_available_stock(product_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT
            SUM(available_stock)

        FROM stock_batches

        WHERE product_id=?

    """,(product_id,))

    stock = cur.fetchone()[0]

    conn.close()

    if stock is None:
        return 0

    return stock

def get_first_available_batch(product_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM stock_batches

        WHERE product_id=?
        AND available_stock>0

        ORDER BY expiry_date,id

        LIMIT 1

    """,(product_id,))

    row = cur.fetchone()

    conn.close()

    return row