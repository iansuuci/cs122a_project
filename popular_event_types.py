from db import get_connection

def popular_event_types(args):
    n = int(args[0])
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.type, COUNT(CASE WHEN s.is_reserved = 1 THEN 1 END) AS reservedCount
            FROM Event e
            LEFT JOIN Slot s ON e.eid = s.eid
            GROUP BY e.type
            HAVING reservedCount >= %s
            ORDER BY reservedCount DESC, e.type ASC
        """, (n,))
        return cur.fetchall()
    finally:
        if conn:
            conn.close()