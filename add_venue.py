from db import get_connection, out_bool, to_bool

def add_venue(args):
    # args: [eid, vid, is_primary]
    eid, vid, is_primary = args[0], args[1], args[2]
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
            (eid, vid, to_bool(is_primary))
        )
        conn.commit()
        out_bool(True)
    except Exception:
        if conn:
            conn.rollback()
        out_bool(False)
    finally:
        if conn:
            conn.close()
