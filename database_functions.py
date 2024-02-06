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


def create_table_job_list(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
    job_id INTEGER NOT NULL PRIMARY KEY,
    job_title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    job_description TEXT NOT NULL,
    job_location TEXT NOT NULL,
    job_remote TEXT NOT NULL,
    job_age TEXT NOT NULL,
    salary TEXT DEFAULT NULL,
    job_link TEXT DEFAULT NULL,
    job_qualification TEXT NOT NULL
    );''')
    cursor.execute('''DELETE FROM jobs''')


def create_table_job_links(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_links(
        link_id INTEGER PRIMARY KEY AUTOINCREMENT,
        link_name TEXT DEFAULT NULL,
        FOREIGN KEY(link_name) REFERENCES jobs(job_link)
        ON DELETE CASCADE ON UPDATE NO ACTION
        );''')
    cursor.execute('''DELETE FROM job_links''')


def create_table_job_qualifications(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_qualifications(
        qualification_id INTEGER PRIMARY KEY,
        qualifications_name TEXT NOT NULL,
        FOREIGN KEY (qualifications_name) REFERENCES jobs(job_qualification)
        ON DELETE CASCADE ON UPDATE NO ACTION
        );''')
    cursor.execute('''DELETE FROM job_qualifications''')


def setup_db(cursor: sqlite3.Cursor):
    create_table_job_links(cursor)
    create_table_job_qualifications(cursor)
    create_table_job_list(cursor)


def insert_data_to_table(cursor: sqlite3.Cursor, json_data):
    for job_entry in json_data:
        cursor.execute('''INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (
                           None,
                           job_entry.get('title', None),
                           job_entry.get('company_name', None),
                           job_entry.get('description', None),
                           job_entry.get('location', None),
                           find_remote_in_job(job_entry),
                           find_job_age(job_entry),
                           find_job_salary(job_entry),
                            "Shish",
                            "shash"))


def find_remote_in_job(job_entry):
    job_extensions = job_entry.get('detected_extensions')
    work_from_home = job_extensions.get('work_from_home', None)
    if work_from_home is None:
        return 'No'
    if work_from_home == 'True':
        return 'Yes'
    return 'No'


def find_job_age(job_entry):
    job_extensions = job_entry.get('detected_extensions')
    posted_at = job_extensions.get('posted_at', None)
    if posted_at is None:
        return "NA"
    return posted_at


def find_job_salary(job_entry):
    job_highlights = job_entry.get('job_highlights', None)
    if job_highlights is None:
        return 'No Salary Specified'
    benefits = None
    for highlight in job_highlights:
        if highlight.get('title') == 'Benefits':
            benefits = highlight
    if benefits is None:
        return 'No Salary Specified'
    for benefit in benefits:
        if 'salary' in benefit.lower():
            return benefit
    return 'No Salary Specified'


def db_close(db_connection: sqlite3.Connection):
    db_connection.commit()
    db_connection.close()
