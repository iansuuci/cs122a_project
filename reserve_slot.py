from db import get_connection, out_bool

def reserve_slot(eid, snum, uid):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Slot SET is_reserved = 1, uid = %s WHERE eid = %s AND snum = %s AND is_reserved = 0",(uid, eid, snum))
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
