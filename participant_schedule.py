from db import get_connection


def participant_schedule(args):
    uid = int(args[0])

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.eid, e.title, e.type, e.datetime, s.snum,
                   v.vid, v.street, v.city, v.state, v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN Hosting h ON e.eid = h.eid AND h.is_primary = 1
            LEFT JOIN Venue v ON h.vid = v.vid
            WHERE s.uid = %s AND s.is_reserved = 1
            ORDER BY e.datetime ASC
            """,
            (uid,),
        )
        return cur.fetchall()
    finally:
        if conn:
            conn.close()
