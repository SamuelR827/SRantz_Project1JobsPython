""" This is the module which handles setting up a sqlite database, creating
tables for the jobs data and inserting that data into the tables."""

import sqlite3
from typing import Tuple, List, Dict, Any

from util_functions import find_job_age
from util_functions import find_job_links
from util_functions import find_job_qualifications
from util_functions import find_job_rate
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
        job_id TEXT NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        remote TEXT NOT NULL,
        posted TEXT NOT NULL,
        salary_min INTEGER NOT NULL,
        salary_max INTEGER NOT NULL,
        salary_rate TEXT NOT NULL
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
            job_id TEXT NOT NULL,
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
            job_id TEXT NOT NULL,
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


def insert_link_to_table(cursor: sqlite3.Cursor, job_id: str, link_dict: List[Dict[str, str]]) -> None:
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


def insert_qualifications_to_table(cursor: sqlite3.Cursor, job_id: str, qualification_list: List[str]) -> None:
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


def get_job_search_data(job_entry: Dict[str, Any]) -> tuple[Any | None, str, str, str, str, str, str, int, int, str]:
    """ This function collects all the data for the specified job entry and returns data
    as a tuple. """
    salary_min, salary_max = find_job_salary(job_entry)
    job_id = job_entry.get('job_id')
    job_title = job_entry.get('title', 'No Title Specified')
    company_name = job_entry.get('company_name', 'No Company Specified')
    job_description = job_entry.get('description', 'No Description Specified')
    job_location = job_entry.get('location', 'No Location Specified')
    job_remote = find_remote_in_job(job_entry)
    job_age = find_job_age(job_entry)
    salary_rate = find_job_rate(salary_min)
    job_data = (
        job_id, job_title, company_name, job_description, job_location, job_remote, job_age, salary_min, salary_max,
        salary_rate)
    return job_data


def insert_job_data_to_table(cursor: sqlite3.Cursor, job_entry: Dict[str, Any]) -> str:
    """This function inserts the data collected from the job_entry dictionary into the table.
    Three find_job functions are called to find the values of remote, age, and salary.
    If a database error occurs an exception will be caught and printed. The data collected is formatted
    as a tuple. """
    job_data = get_job_search_data(job_entry)
    try:
        statement = '''INSERT OR IGNORE INTO jobs (job_id, title, company, description, location, 
        remote, posted, salary_min, salary_max, salary_rate)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        cursor.execute(statement, job_data)
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    return job_data[0]


def save_searched_data_to_database(cursor: sqlite3.Cursor, json_data: List[Dict[str, Any]]) -> None:
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


def insert_worksheet_data_to_database(cursor: sqlite3.Cursor, job_data):
    try:
        statement = '''INSERT OR IGNORE INTO jobs (job_id, title, company, description, location, 
        remote, posted, salary_min, salary_max, salary_rate)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        cursor.execute(statement, job_data)
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
