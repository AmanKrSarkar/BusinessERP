import sqlite3
import os

DB_FOLDER = "data"
DB_NAME = "business.db"

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Parties Master
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        party_name TEXT UNIQUE,
        party_type TEXT,
        mobile TEXT,
        gstin TEXT,
        state TEXT,
        address TEXT,
        opening_balance REAL DEFAULT 0,
        status TEXT DEFAULT 'Active'
    )
    """)

    # -----------------------------
    # Products Master
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT UNIQUE,
        company TEXT,
        hsn_code TEXT,
        gst_percent REAL,
        low_stock INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Active',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # Purchase Bills
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE,
        invoice_date TEXT,

        party_id INTEGER,

        gross_amount REAL,
        other_charges REAL,
        round_off REAL,
        net_amount REAL,

        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(party_id) REFERENCES parties(id)
    )
    """)

    # -----------------------------
    # Purchase Items
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        purchase_bill_id INTEGER,

        product_id INTEGER,

        batch_id INTEGER,

        qty REAL,

        free_qty REAL,

        rate REAL,

        disc1 REAL,

        disc2 REAL,

        gst REAL,

        taxable REAL,

        total REAL,

        FOREIGN KEY(purchase_bill_id) REFERENCES purchase_bills(id),

        FOREIGN KEY(product_id) REFERENCES products(id),

        FOREIGN KEY(batch_id) REFERENCES stock_batches(id)

    )
    """)

    # -----------------------------
    # Stock Batches
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_batches (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_id INTEGER,

        batch_name TEXT,

        expiry_date TEXT,

        mrp REAL,

        rate REAL,

        qty REAL,

        free_qty REAL,

        available_stock REAL,

        purchase_bill_id INTEGER,

        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(product_id) REFERENCES products(id),

        FOREIGN KEY(purchase_bill_id) REFERENCES purchase_bills(id)

    )
    """)

    # -----------------------------
    # Sales Bills
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_bills (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT UNIQUE,

        invoice_date TEXT,

        party_id INTEGER,

        gross_amount REAL,

        other_charges REAL,

        round_off REAL,

        net_amount REAL,

        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(party_id) REFERENCES parties(id)

    )
    """)

    # -----------------------------
    # Sales Items
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        sales_bill_id INTEGER,

        product_id INTEGER,

        batch_id INTEGER,

        qty REAL,

        rate REAL,

        disc1 REAL,

        disc2 REAL,

        gst REAL,

        taxable REAL,

        total REAL,

        FOREIGN KEY(sales_bill_id) REFERENCES sales_bills(id),

        FOREIGN KEY(product_id) REFERENCES products(id),

        FOREIGN KEY(batch_id) REFERENCES stock_batches(id)

    )
    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS payments(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    party_id INTEGER,

    payment_date TEXT,

    payment_type TEXT,

    amount REAL,

    remarks TEXT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(party_id) REFERENCES parties(id)

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS purchase_returns(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    bill_no TEXT,

    party_id INTEGER,

    return_date TEXT,

    total REAL,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(party_id) REFERENCES parties(id)

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS sales_returns(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    invoice_no TEXT,

    party_id INTEGER,

    return_date TEXT,

    total REAL,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(party_id) REFERENCES parties(id)

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS stock_adjustments(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    product_id INTEGER,

    batch_id INTEGER,

    qty REAL,

    reason TEXT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS company(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_name TEXT,

    address TEXT,

    mobile TEXT,

    email TEXT,

    gstin TEXT

    )

    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully.")