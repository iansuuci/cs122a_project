from db import get_connection


def update_event(args):
    # args: [eid, title, datetime]
    eid = int(args[0])
    title = args[1]
    event_datetime = args[2]

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Event SET title = %s, datetime = %s WHERE eid = %s",
            (title, event_datetime, eid),
        )
        if cur.rowcount > 0:
            conn.commit()
            return True
        conn.rollback()
        return False
    except Exception:
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
