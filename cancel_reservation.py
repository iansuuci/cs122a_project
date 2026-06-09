from db import get_connection

def cancel_reservation(args):
    eid = int(args[0])
    snum = int(args[1])
    uid = int(args[2])

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Slot SET is_reserved = 0, uid = NULL WHERE eid = %s AND snum = %s AND uid = %s AND is_reserved = 1",(eid, snum, uid))
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