from database.database import get_connection


def save_reference(category, name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO reference_master
        (
            category,
            name
        )

        VALUES(?,?)

    """, (category, name))

    conn.commit()
    conn.close()


def get_reference_names(category):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT name

        FROM reference_master

        WHERE category=?

        AND status='Active'

        ORDER BY name

    """, (category,))

    rows = cur.fetchall()

    conn.close()

    return [row["name"] for row in rows]


def reference_exists(category, name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT id

        FROM reference_master

        WHERE category=?

        AND LOWER(name)=LOWER(?)

    """, (category, name))

    row = cur.fetchone()

    conn.close()

    return row is not None


def get_references(category):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM reference_master

        WHERE category=?

        ORDER BY name

    """, (category,))

    rows = cur.fetchall()

    conn.close()

    return rows

def update_reference(ref_id, category, name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE reference_master

        SET
            category=?,
            name=?

        WHERE id=?

    """, (
        category,
        name,
        ref_id
    ))

    conn.commit()
    conn.close()

def delete_reference(ref_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        DELETE FROM reference_master

        WHERE id=?

    """, (ref_id,))

    conn.commit()
    conn.close()