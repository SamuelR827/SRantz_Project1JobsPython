""" This is the module which handles setting up a sqlite database, creating
tables for the jobs data and inserting that data into the tables."""

import sqlite3
from typing import Tuple, List, Dict, Any

from util_functions import find_job_age
from util_functions import find_job_links
from util_functions import find_job_qualifications
from util_functions import find_job_salary
from util_functions import find_remote_in_job


def create_db_connection(db_file: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """ This function establishes a connection with the sqlite database
    returning a connection and cursor object as a tuple.
    If a database error occurs an exception will be caught and printed"""
    # start with empty cursor and connection objects
    db_connection = None
    db_cursor = None
    # try to connect to db and create cursor object
    try:
        db_connection = sqlite3.connect(db_file)
        db_cursor = db_connection.cursor()
    # catch db error
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    # return connection and cursor, if error occurred they will be empty
    finally:
        return db_connection, db_cursor


def create_table_job_list(cursor: sqlite3.Cursor) -> None:
    """ This function creates a table for the main jobs data, with job_id as a primary
    autoincrement key. Other information such as title, company, description, remote,
    posted, salary will be text. The function
    will delete all the existing data from the table. So that everytime the program is
    run new data will be generated and replaced.If a database error occurs an exception will be caught and printed."""
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
        job_id INTEGER NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        remote TEXT NOT NULL,
        posted TEXT NOT NULL,
        salary_min TEXT DEFAULT NULL
        salary_max TEXT DEFAULT NULL
        
        );''')
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')


def create_table_job_links(cursor: sqlite3.Cursor) -> None:
    """ This function creates a table for the job_links data, with link_id as a primary
       autoincrement key. Other information such as job_id as foreign key to correspond each link
       with a job. Each link will be a separate row in the database as text.
       The function will delete all the existing data from the table. So that everytime the program is
        run new data will be generated and replaced.
       If a database error occurs an exception will be caught and printed."""
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS job_links(
            job_id INTEGER NOT NULL,
            link_id INTEGER NOT NULL PRIMARY KEY ,
            link TEXT DEFAULT NULL,
            FOREIGN KEY(job_id) REFERENCES jobs(job_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
            );''')
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')


def create_table_job_qualifications(cursor: sqlite3.Cursor) -> None:
    """ This function creates a table for the job_qualifications data, with qualification_id as a primary
           autoincrement key. Other information such as job_id as foreign key to correspond each qualification
           with a job. Each qualification will be a separate row in the database as text. The function
           will delete all the existing data from the table. So that everytime the program is
           run new data will be generated and replaced.
           If a database error occurs an exception will be caught and printed."""
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS job_qualifications(
            job_id INTEGER NOT NULL,
            qualification_id INTEGER NOT NULL PRIMARY KEY,
            qualification TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
            );''')
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')


def setup_db(cursor: sqlite3.Cursor) -> None:
    """ This function calls all the create table functions that are needed
    for this database."""
    create_table_job_links(cursor)
    create_table_job_qualifications(cursor)
    create_table_job_list(cursor)


def insert_link_to_table(cursor: sqlite3.Cursor, job_id: int, link_dict: List[Dict[str, str]]) -> None:
    """ This function will insert each link from a specified job into the job_link table. The links
    are a list of dictionaries. It will loop through each dictionary and get the value of the key
    link which contains the actual link as text. The link is inserted into the table.
    Job_id is passed a parameter to correspond each link with the right job as foreign key.
    If a database error occurs an exception will be caught and printed. """
    for link in link_dict:
        try:
            cursor.execute('''INSERT INTO job_links(job_id, link) VALUES (?, ?)''',
                           (job_id,
                            link.get('link')))
        except sqlite3.Error as db_error:
            print(f'A database error has occurred: {db_error}')


def insert_qualifications_to_table(cursor: sqlite3.Cursor, job_id: int, qualification_list: List[str]) -> None:
    """ This function will insert each qualification from a specified job into the job_qualification table.
    The qualifications are a list of strings. The function loops through each string and insert
    that string into the table. Job_id is passed as a parameter to correspond each qualification
    with the right job as foreign key. If a database error occurs an exception will be caught and printed. """
    for qualification in qualification_list:
        try:
            cursor.execute('''INSERT INTO job_qualifications(job_id, qualification) VALUES (?, ?)''',
                           (job_id, qualification))
        except sqlite3.Error as db_error:
            print(f'A database error has occurred: {db_error}')


def insert_job_data_to_table(cursor: sqlite3.Cursor, job_entry: Dict[str, Any]) -> int:
    """This function inserts the data collected from the job_entry dictionary into the table.
    Three find_job functions are called to find the values of remote, age, and salary.
    If a database error occurs an exception will be caught and printed. """
    try:
        cursor.execute(
            '''INSERT INTO jobs (title, company, description, location, remote, posted, salary)
            VALUES(?, ?, ?, ?, ?, ?, ?)''',
            (
                job_entry.get('title', 'No Title Specified'),
                job_entry.get('company_name', 'No Company Specified'),
                job_entry.get('description', 'No Description Specified'),
                job_entry.get('location', 'No Location Specified'),
                find_remote_in_job(job_entry),
                find_job_age(job_entry),
                find_job_salary(job_entry)))
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    return cursor.lastrowid


def save_searched_data_to_database(cursor: sqlite3.Cursor, json_data: List[Dict[str, Any]], job_workbook) -> None:
    """ This function will loop through each job_entry. Find the links
    and qualifications of that job by calling find_job functions and insert the data
    to corresponding tables by calling the insert data to table functions.
    The main table returns the corresponding job_id after each insert for the other tables to use
    as a foreign key."""
    for job_entry in json_data:
        job_id = insert_job_data_to_table(cursor, job_entry)
        job_qualifications = find_job_qualifications(job_entry)
        job_links = find_job_links(job_entry)
        insert_qualifications_to_table(cursor, job_id, job_qualifications)
        insert_link_to_table(cursor, job_id, job_links)


def insert_worksheet_data_to_database(cursor: sqlite3.Cursor, job_name, company_name, location, posted_ago, salary):
    try:
        cursor.execute(
            '''INSERT INTO jobs (title, company, description, location, remote, posted, salary)
            VALUES(?, ?, ?, ?, ?, ?, ?)''',
            (
                job_name,
                company_name,
                'No description Specified',
                location,
                'NA',
                posted_ago,
                salary))
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')


def db_close(db_connection: sqlite3.Connection) -> None:
    """ This function will commit and close the database.
    If a database error occurs an exception will be caught and printed
    """
    try:
        db_connection.commit()
        db_connection.close()
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
