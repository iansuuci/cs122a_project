from db import get_connection, out_table
 
def organizer_stats(args):
    # args: [N]
    n = int(args[0])
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.creator_uid,
                   COUNT(DISTINCT e.eid),
                   COUNT(CASE WHEN s.is_reserved = 1 THEN 1 END)
            FROM Event e
            LEFT JOIN Slot s ON e.eid = s.eid
            GROUP BY e.creator_uid
            HAVING COUNT(DISTINCT e.eid) >= %s
            ORDER BY COUNT(DISTINCT e.eid) DESC, e.creator_uid ASC
        """, (n,))
        out_table(cur.fetchall())
    finally:
        if conn:
            conn.close()
