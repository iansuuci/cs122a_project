from db import get_connection, out_table
 
def organizer_stats(args):
    # args: [N]
    n = int(args[0])
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.uid, u.username, o.department, COUNT(e.eid) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            JOIN Event e ON e.creator_uid = o.uid
            GROUP BY o.uid, u.username, o.department
            HAVING COUNT(e.eid) >= %s
            ORDER BY eventCount DESC, o.uid ASC
        """, (n,))

        return cur.fetchall()
    finally:
        if conn:
            conn.close()
