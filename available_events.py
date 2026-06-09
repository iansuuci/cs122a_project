from db import get_connection, out_table

def available_events(args):
    # args: [date]
    date = args[0]
    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.eid, e.title, e.type, e.datetime, COUNT(*) AS availableSlots
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE
                e.datetime >= DATE_ADD(%s, INTERVAL 1 DAY)
                AND s.is_reserved = 0
            GROUP BY e.eid, e.title, e.type, e.datetime
            ORDER BY
                e.datetime ASC,
                e.eid ASC
        """, (date,))
        out_table(cur.fetchall())
    finally:
        if conn:
            conn.close()
