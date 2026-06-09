from db import get_connection

def reserve_slot(args):
    eid = int(args[0])
    snum = int(args[1])
    uid = int(args[2])

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Slot SET is_reserved = 1, uid = %s WHERE eid = %s AND snum = %s AND is_reserved = 0", (uid, eid, snum))
        if cur.rowcount > 0:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False
    except Exception:
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()