import mysql.connector


def get_connection():
    return mysql.connector.connect(
        user="test",
        password="password",
        database="cs122a"
    )

def out_bool(ok):
    print("Success" if ok else "Fail")

def out_table(rows):
    for r in rows:
        print(",".join("NULL" if v is None else str(v) for v in r))

def to_none(v):
    return None if v == "NULL" else v

def to_bool(v):
    return 1 if str(v).lower() == "true" else 0
