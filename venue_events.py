from db import get_connection


def venue_events(args):
    vid = int(args[0])

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT Event.eid, Event.title, Event.type, Event.datetime, Hosting.is_primary
        FROM Event
        JOIN Hosting ON Event.eid = Hosting.eid
        WHERE Hosting.vid = %s
        ORDER BY Event.datetime ASC, Event.eid ASC
        """,
        (vid,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows