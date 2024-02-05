import sqlite3
from typing import Tuple


def create_db_connection(db_file: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = None
    db_cursor = None
    try:
        db_connection = sqlite3.connect(db_file)
        db_cursor = db_connection.cursor()
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    finally:
        return db_connection, db_cursor


def db_close(db_connection: sqlite3.Connection):
    db_connection.commit()
    db_connection.close()


def create_table_job_list(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
    job_id INTEGER PRIMARY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    job_description TEXT NOT NULL,
    job_location TEXT NOT NULL,
    job remote BOOLEAN,
    job_age TEXT NOT NULL,
    salary TEXT,
    job_link TEXT,
    job_qualification TEXT,
    FOREIGN KEY(job_link) REFERENCES job_links(link_name)
    ON DELETE CASECADE ON UPDATE NO ACTION,
    FOREIGN KEY (job_qualification) REFERENCES job_qualifcations(qualifications_name)
    ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def create_table_job_links(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_links(
        link_id INTEGER PRIMARY AUTOINCREMENT,
        link_name TEXT
        );''')


def create_table_job_qualifications(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_qualifications(
        qualification_id INTEGER PRIMARY AUTOINCREMENT,
        qualifications_name TEXT NOT NULL
        );''')


def setup_db(cursor: sqlite3.Cursor):
    create_table_job_links(cursor)
    create_table_job_qualifications(cursor)
    create_table_job_list(cursor)
