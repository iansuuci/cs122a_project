from db import get_connection


def delete_organizer(args):
    uid = int(args[0])

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM Organizer WHERE uid = %s",
            (uid,)
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()