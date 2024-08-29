import os
import sqlite3


def initialize_database(db_name='../data/park_smart.db'):
    """
    Initializes the SQLite database for storing parking records.

    Args:
        db_name (str): Name of the database file.

    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    # Construct the full path to the database file
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, db_name)

    # Ensure the data directory exists
    data_dir = os.path.dirname(db_path)
    os.makedirs(data_dir, exist_ok=True)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table for parking records if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        car_number TEXT,
        report_date TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    return conn


def insert_record(conn, image_path, car_number, report_date, status):
    """
    Inserts a new parking record into the database.

    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        image_path (str): Path to the parking image.
        car_number (str): Identified car number.
        report_date (str): Date of the parking record.
        status (str): Current status of the parking record.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO parking_records (image_path, car_number, report_date, status)
    VALUES (?, ?, ?, ?)
    ''', (image_path, car_number, report_date, status))
    conn.commit()


def fetch_records(conn, status_filter=None):
    """
    Fetches parking records from the database.

    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        status_filter (str, optional): Status filter for fetching records. Defaults to None.

    Returns:
        list: List of fetched parking records.
    """
    cursor = conn.cursor()
    if status_filter:
        cursor.execute('SELECT * FROM parking_records WHERE status=?', (status_filter,))
    else:
        cursor.execute('SELECT * FROM parking_records')
    return cursor.fetchall()
