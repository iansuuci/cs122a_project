from db import get_connection, out_bool

def cancel_reservation(eid, snum, uid):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Slot SET is_reserved = 0, uid = NULL WHERE eid = %s AND snum = %s AND uid = %s AND is_reserved = 1",(eid, snum, uid))
        if cur.rowcount > 0:
            conn.commit()
            out_bool(True)
        else:
            conn.rollback()
            out_bool(False)
    except Exception:
        if conn:
            conn.rollback()
        out_bool(False)
    finally:
        if conn:
            conn.close()