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
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    remote TEXT NOT NULL,
    posted TEXT NOT NULL,
    salary TEXT DEFAULT NULL
    );''')
    cursor.execute('''DELETE FROM jobs''')


def create_table_job_links(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_links(
        job_id INTEGER NOT NULL,
        link_id INTEGER NOT NULL PRIMARY KEY ,
        link TEXT DEFAULT NULL,
        FOREIGN KEY(job_id) REFERENCES jobs(job_id)
        ON DELETE CASCADE ON UPDATE NO ACTION
        );''')
    cursor.execute('''DELETE FROM job_links''')


def create_table_job_qualifications(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_qualifications(
        job_id INTEGER NOT NULL,
        qualification_id INTEGER NOT NULL PRIMARY KEY,
        qualification TEXT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        ON DELETE CASCADE ON UPDATE NO ACTION
        );''')
    cursor.execute('''DELETE FROM job_qualifications''')


def setup_db(cursor: sqlite3.Cursor):
    create_table_job_links(cursor)
    create_table_job_qualifications(cursor)
    create_table_job_list(cursor)


def insert_link_to_table(cursor: sqlite3.Cursor, job_id, link_list):
    for link in link_list:
        cursor.execute('''INSERT INTO job_links(job_id, link) VALUES (?, ?)''',
                       (job_id,
                        link))


def insert_qualifications_to_table(cursor: sqlite3.Cursor, job_id, qualification_list):
    for qualification in qualification_list:
        cursor.execute('''INSERT INTO job_qualifications(job_id, qualification) VALUES (?, ?)''',
                       (job_id, qualification))


def insert_job_data_to_table(cursor: sqlite3.Cursor, job_entry):
    cursor.execute(
        '''INSERT INTO jobs (title, company, description, location, remote, posted, salary) 
        VALUES(?, ?, ?, ?, ?, ?, ?)''',
        (
            job_entry.get('title', None),
            job_entry.get('company_name', None),
            job_entry.get('description', None),
            job_entry.get('location', None),
            find_remote_in_job(job_entry),
            find_job_age(job_entry),
            find_job_salary(job_entry)))
    return cursor.lastrowid


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
    for highlight in job_highlights:
        if highlight.get('title') == 'Benefits':
            benefits = highlight.get('items', [])
            for benefit in benefits:
                if 'salary:' in benefit.lower() or 'pay:' in benefit.lower() or '$' in benefit:
                    return benefit.strip()
            return 'No Salary Specified'
    return 'No Salary Specified'


def db_close(db_connection: sqlite3.Connection):
    db_connection.commit()
    db_connection.close()
