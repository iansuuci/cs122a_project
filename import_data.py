import csv
import os

from db import get_connection


TABLES_TO_DROP = [
    "Approval",
    "Hosting",
    "OffCampus",
    "OnCampus",
    "Venue",
    "Slot",
    "Event",
    "Administrator",
    "Participant",
    "Organizer",
    "User",
]


CREATE_TABLE_STATEMENTS = [
    """
    CREATE TABLE User (
        uid INT,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        joined DATE NOT NULL,
        PRIMARY KEY (uid)
    )
    """,

    """
    CREATE TABLE Organizer (
        uid INT,
        department TEXT NOT NULL,
        experience INT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Participant (
        uid INT,
        type TEXT,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Administrator (
        uid INT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Event (
        eid INT,
        creator_uid INT NOT NULL,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        datetime DATETIME NOT NULL,
        PRIMARY KEY (eid),
        FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Slot (
        eid INT,
        snum INT NOT NULL,
        is_reserved BOOLEAN NOT NULL,
        uid INT,
        PRIMARY KEY (eid, snum),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Venue (
        vid INT,
        street TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL,
        PRIMARY KEY (vid)
    )
    """,

    """
    CREATE TABLE OnCampus (
        vid INT,
        code TEXT NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE OffCampus (
        vid INT,
        distance INT NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Hosting (
        eid INT NOT NULL,
        vid INT NOT NULL,
        is_primary BOOLEAN NOT NULL,
        PRIMARY KEY (eid, vid),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE Approval (
        uid INT NOT NULL,
        vid INT NOT NULL,
        valid_from DATE NOT NULL,
        valid_until DATE NOT NULL,
        PRIMARY KEY (uid, vid),
        FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
    )
    """,
]


CSV_IMPORTS = [
    ("User.csv", "User", 4),
    ("Organizer.csv", "Organizer", 3),
    ("Participant.csv", "Participant", 2),
    ("Administrator.csv", "Administrator", 3),
    ("Event.csv", "Event", 5),
    ("Slot.csv", "Slot", 4),
    ("Venue.csv", "Venue", 5),
    ("OnCampus.csv", "OnCampus", 2),
    ("OffCampus.csv", "OffCampus", 2),
    ("Hosting.csv", "Hosting", 3),
    ("Approval.csv", "Approval", 4),
]


def load_csv_file(cursor, folder_name, file_name, table_name, column_count):
    file_path = os.path.join(folder_name, file_name)
    placeholders = ", ".join(["%s"] * column_count)
    insert_statement = f"INSERT INTO {table_name} VALUES ({placeholders})"

    with open(file_path) as csv_file:
        for row in csv.reader(csv_file):
            row = [None if value == "NULL" else value for value in row]
            cursor.execute(insert_statement, row)


def import_data(args):
    folder_name = args[0]

    connection = get_connection()
    cursor = connection.cursor()

    try:
        for table_name in TABLES_TO_DROP:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        for create_statement in CREATE_TABLE_STATEMENTS:
            cursor.execute(create_statement)

        for file_name, table_name, column_count in CSV_IMPORTS:
            load_csv_file(
                cursor,
                folder_name,
                file_name,
                table_name,
                column_count,
            )

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()