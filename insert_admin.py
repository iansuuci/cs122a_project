from db import get_connection


def insert_admin(args):
    # args: [uid, email, username, joined, firstname, lastname]
    uid = int(args[0])
    email = args[1]
    username = args[2]
    joined = args[3]
    firstname = args[4]
    lastname = args[5]

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
            (uid, email, username, joined),
        )
        cur.execute(
            "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
            (uid, firstname, lastname),
        )
        conn.commit()
        return True
    except Exception:
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
