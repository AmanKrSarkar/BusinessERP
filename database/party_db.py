from database.database import get_connection


# ==========================================
# GET PARTY
# ==========================================

def get_party(party_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM parties
        WHERE party_name = ?
    """, (party_name,))

    row = cur.fetchone()

    conn.close()

    return row


# ==========================================
# SEARCH PARTIES
# ==========================================

def search_parties(keyword):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM parties
        WHERE party_name LIKE ?
        ORDER BY party_name
        LIMIT 20
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================
# PARTY EXISTS
# ==========================================

def party_exists(party_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM parties
        WHERE party_name = ?
    """, (party_name,))

    exists = cur.fetchone()[0] > 0

    conn.close()

    return exists

def get_party_names():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT party_name
        FROM parties
        ORDER BY party_name
    """)

    names = [row["party_name"] for row in cur.fetchall()]

    conn.close()

    return names