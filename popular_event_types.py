from db import get_connection

def popular_event_types(args):
    n = int(args[0])
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.type, COUNT(*)
            FROM Event e JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = 1
            GROUP BY e.type
            HAVING COUNT(*) >= %s
            ORDER BY COUNT(*) DESC, e.type ASC
        """, (n,))
        return cur.fetchall()
    finally:
        if conn:
            conn.close()