import sqlite3

from database.database import get_connection


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# PARTY
# ==========================================

def get_or_create_party(name, mobile, gstin, address):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM parties WHERE party_name=?",
        (name,)
    )

    row = cur.fetchone()

    if row:

        party_id = row["id"]

        cur.execute("""
            UPDATE parties
            SET mobile=?,
                gstin=?,
                address=?
            WHERE id=?
        """, (
            mobile,
            gstin,
            address,
            party_id
        ))

        conn.commit()
        conn.close()

        return party_id

    cur.execute("""
        INSERT INTO parties
        (
            party_name,
            party_type,
            mobile,
            gstin,
            address
        )
        VALUES
        (
            ?, 'Supplier', ?, ?, ?
        )
    """, (
        name,
        mobile,
        gstin,
        address
    ))

    party_id = cur.lastrowid

    conn.commit()
    conn.close()

    return party_id


# ==========================================
# PRODUCT
# ==========================================

def get_or_create_product(
    product_name,
    company,
    hsn,
    gst
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM products
        WHERE product_name=?
    """, (
        product_name,
    ))

    row = cur.fetchone()

    if row:

        conn.close()
        return row["id"]

    cur.execute("""
        INSERT INTO products
        (
            product_name,
            company,
            hsn_code,
            gst_percent
        )
        VALUES
        (
            ?, ?, ?, ?
        )
    """, (
        product_name,
        company,
        hsn,
        gst
    ))

    product_id = cur.lastrowid

    conn.commit()
    conn.close()

    return product_id

# ==========================================
# BATCH
# ==========================================

def get_or_create_batch(
    product_id,
    batch_name,
    expiry_date,
    mrp,
    rate,
    qty,
    free_qty,
    purchase_bill_id
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, available_stock
        FROM stock_batches
        WHERE product_id=?
        AND batch_name=?
        AND expiry_date=?
        AND mrp=?
        AND rate=?
    """, (
        product_id,
        batch_name,
        expiry_date,
        mrp,
        rate
    ))

    row = cur.fetchone()

    if row:

        batch_id = row["id"]

        new_stock = row["available_stock"] + qty + free_qty

        cur.execute("""
            UPDATE stock_batches
            SET
                qty = qty + ?,
                free_qty = free_qty + ?,
                available_stock = ?
            WHERE id=?
        """, (
            qty,
            free_qty,
            new_stock,
            batch_id
        ))

        conn.commit()
        conn.close()

        return batch_id

    cur.execute("""
        INSERT INTO stock_batches
        (
            product_id,
            batch_name,
            expiry_date,
            mrp,
            rate,
            qty,
            free_qty,
            available_stock,
            purchase_bill_id
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?
        )
    """, (
        product_id,
        batch_name,
        expiry_date,
        mrp,
        rate,
        qty,
        free_qty,
        qty + free_qty,
        purchase_bill_id
    ))

    batch_id = cur.lastrowid

    conn.commit()
    conn.close()

    return batch_id


# ==========================================
# PURCHASE BILL
# ==========================================

def create_purchase_bill(
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
        INSERT INTO purchase_bills
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
    """, (
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
# PURCHASE ITEMS
# ==========================================

def save_purchase_item(
    purchase_bill_id,
    product_id,
    batch_id,
    qty,
    free_qty,
    rate,
    disc1,
    disc2,
    gst,
    taxable,
    total
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO purchase_items
        (
            purchase_bill_id,
            product_id,
            batch_id,
            qty,
            free_qty,
            rate,
            disc1,
            disc2,
            gst,
            taxable,
            total
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?,?
        )
    """, (
        purchase_bill_id,
        product_id,
        batch_id,
        qty,
        free_qty,
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
# CHECK DUPLICATE INVOICE
# ==========================================

def invoice_exists(invoice_number):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM purchase_bills
        WHERE invoice_number = ?
    """, (invoice_number,))

    exists = cur.fetchone()[0] > 0

    conn.close()

    return exists