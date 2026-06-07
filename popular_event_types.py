from db import get_connection, out_table

def popular_event_types(n):
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
        out_table(cur.fetchall())
    finally:
        if conn:
            conn.close()