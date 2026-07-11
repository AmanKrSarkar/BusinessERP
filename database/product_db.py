from database.database import get_connection


# ==========================================
# SEARCH PRODUCTS
# ==========================================

def search_products(keyword):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM products
        WHERE product_name LIKE ?
        ORDER BY product_name
        LIMIT 20
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================
# GET PRODUCT DETAILS
# ==========================================

def get_product(product_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM products
        WHERE product_name = ?
    """, (product_name,))

    row = cur.fetchone()

    conn.close()

    return row


# ==========================================
# PRODUCT EXISTS
# ==========================================

def product_exists(product_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE product_name = ?
    """, (product_name,))

    exists = cur.fetchone()[0] > 0

    conn.close()

    return exists

# ==========================================
# PRODUCT LIST
# ==========================================

def get_product_names():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT product_name
        FROM products
        ORDER BY product_name
    """)

    names = [row["product_name"] for row in cur.fetchall()]

    conn.close()

    return names

def get_product_by_name(product_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM products
        WHERE product_name=?
    """,(product_name,))

    row = cur.fetchone()

    conn.close()

    return row