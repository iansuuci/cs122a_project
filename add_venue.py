from db import get_connection

def add_venue(args):
    # args: [eid, vid, is_primary]
    eid, vid = int(args[0]), int(args[1])
    is_primary = 1 if args[2].lower() == "true" else 0
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        if is_primary:
            cur.execute("""
                        SELECT 1
                        FROM Hosting
                        WHERE eid = %s
                        AND is_primary = 1
                        """, (eid,))
            if cur.fetchone() is not None:
                return False
        cur.execute(
            "INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
            (eid, vid, is_primary)
        )
        conn.commit()
        return True
    except Exception:
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()