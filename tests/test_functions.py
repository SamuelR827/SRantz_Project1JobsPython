""" This module handles automated unit tests. We have five automated tests to make sure
data is properly searched through using serpapi and excel. As well as to make sure this
data is properly inserted into the database. """
from sqlite3 import Connection, Cursor
from typing import Generator, Any

import pytest

import gui.list_window as list_window
from database_functions import create_db_connection
from database_functions import create_table_job_links
from database_functions import create_table_job_list
from database_functions import create_table_job_qualifications
from database_functions import insert_worksheet_data_to_database
from database_functions import save_searched_data_to_database
from excel_functions import add_excel_job_data
from excel_functions import load_job_workbook
from serpAPI import secrets_handling
from serpAPI import serpapi_search


@pytest.fixture(scope="module")
def mock_db_connection():
    """ This function creates a mock database for testing the function
    that saves data to the database."""
    # create a mock db_file
    db_file = 'test_results.db'
    # create a mock connection and cursor
    test_connection, test_cursor = create_db_connection(db_file)

    # create mock tables by calling database create tables function
    create_table_job_qualifications(test_cursor)
    create_table_job_links(test_cursor)
    create_table_job_list(test_cursor)

    # teardown/cleanup of connection and cursor
    yield test_connection, test_cursor
    # commit and close
    test_cursor.close()
    test_connection.commit()
    test_connection.close()


def test_read_excel_sheet():
    """ This test verifies that reading the xlsx sheet work properly. Making
    sure there is at least 300 rows and exactly 10 columns in the sheet."""
    # get excel workbook
    job_worksheet = load_job_workbook('Sprint3Data.xlsx')
    # get row count of Excel worksheet
    row_count = job_worksheet.max_row
    # assert it has at least 300 rows
    assert row_count >= 300
    # get column count of Excel worksheet
    column_count = job_worksheet.max_column
    # assert it has at has 10 columns
    assert column_count == 10


def test_save_excel_data_to_database(mock_db_connection):
    """ This test verifies that saving the xlsx sheet works properly. Making
    sure that all the data in the workbook is added to our test database."""
    # get excel workbook
    job_worksheet = load_job_workbook('Sprint3Data.xlsx')
    # create mock connection and cursor for mock database
    test_connection, test_cursor = mock_db_connection
    # add excel data to mock database
    add_excel_job_data(test_cursor, job_worksheet)
    # get length of database (accounting for duplicates) assert it is 678
    database_list = test_cursor.execute('''SELECT * from jobs''').fetchall()
    assert len(database_list) >= 678


def test_insert_excel_data_to_database(mock_db_connection):
    """ This test verifies that inserting data into our database works by testing
    the insert excel data function. Mock excel data was created to insert and made sure it was
    there. """
    # create mock connection and cursor for mock database
    test_connection, test_cursor = mock_db_connection
    # create test data in tuple form
    test_excel_data = ('some excel job id', 'some excel job title', 'some excel company name', 'N/A',
                       'some excel job location', 'N/A', 'some excel post date', 15, 100, 'hourly')
    # insert excel test data into database
    insert_worksheet_data_to_database(test_cursor, test_excel_data)
    # fetch result inserted and verify it is not null
    test_cursor.execute('''SELECT * FROM jobs WHERE title = "some excel job title"''')
    result = test_cursor.fetchone()
    assert result is not None


def test_save_data_to_database(mock_db_connection: Generator[tuple[Connection, Cursor], Any, None]) -> None:
    """ This function tests the save_data_to_database function. Making
    sure that the database is created properly and inserted with jobs data."""
    # call mock_db_connection to create test cursor and connection
    test_connection, test_cursor = mock_db_connection
    # sample data in json format
    test_json_job_data = [
        {
            "title": "Some Job Title",
            "company_name": "Some Company Name",
            "location": "Some Location",
            "via": "Some Via",
            "description": "Some Description",
            "job_highlights":
                [
                    {
                        "title": "Qualifications",
                        "items": [
                            "Qualification 1", "Qualification 2"
                        ]
                    },
                    {
                        "title": "Responsibilities",
                        "items": [
                            "Responsibility 1", "Responsibility 2"
                        ]
                    },
                    {
                        "title": "Benefits",
                        "items": [
                            "Salary $0 - 100"
                        ]
                    }
                ],
            "related_links": [
                {
                    "link": "https://example.com",
                    "text": "Link Title"
                }],
            "thumbnail": "https://examplethumb.com",
            "extensions":
                [
                    "some time ago",
                    "some information"
                ],
            "detected_extensions": {
                "posted_at": "some time ago"},
            "job_id": "some job id"
        },
    ]
    # call function to test saving data
    save_searched_data_to_database(test_cursor, test_json_job_data)
    # Check if the test data exists in the database
    test_cursor.execute('''SELECT * FROM jobs WHERE title = "Some Job Title"''')
    # fetch the single result and create a variable
    result = test_cursor.fetchone()
    # assert the result is not null
    assert result is not None


def test_search_results_count() -> None:
    """ This function tests to make sure 50 search results are generated with
    serpapi_search when 5 pages are given. Test is a mock form of perform_search
    function in main module. """
    # variable to count the results
    result_count = 0
    # sample query and location
    query = "computer programmer"
    location = "new york"
    # get api key with secret handling
    api_key = secrets_handling()
    # keep track of pages
    page_offset = 0
    # variable to generate 5 pages - 50 results
    num_pages = 5
    # loop based on the amount of pages specified
    for page in range(1, num_pages + 1):
        # call serpapi search with sample query and return jobs_results as json
        search_results_as_json = serpapi_search(query, location, api_key, page, page_offset)
        # count each item in the list jobs_results
        result_count += len(search_results_as_json)
        # increment page offset
        page_offset += 10
    # make sure the result count is greater or equal to 50, print failing message otherwise
    assert result_count >= 50, f"Expected at least 50 data items, but got {result_count}"


def setup_test_filter_data():
    jobs = [
        {
            'job_title': 'Software Engineer',
            'job_description': 'We are hiring a Software Engineer',
            'job_qualifications': ['Python', 'Java'],
            'job_location': 'Boston, MA',
            'job_remote': 'No',
            'salary_min': 80000
        },
        {
            'job_title': 'Data Scientist',
            'job_description': 'We are looking for a Data Scientist',
            'job_qualifications': ['Python', 'R'],
            'job_location': 'New York, NY',
            'job_remote': 'Yes',
            'salary_min': 90000
        },
        {
            'job_title': 'Web Developer',
            'job_description': 'We need a Web Developer with HTML and CSS skills',
            'job_qualifications': ['HTML', 'CSS', 'JavaScript'],
            'job_location': 'San Francisco, CA',
            'job_remote': 'No',
            'salary_min': 85000
        }
    ]
    return jobs


def test_filter_jobs_by_keyword():
    data_to_filter = setup_test_filter_data()
    filtered_jobs = list_window.JobsListWindow.filter_jobs_by_keyword(data_to_filter, 'Python')
    assert len(filtered_jobs) == 2  # Expecting 2 jobs matching keyword 'Engineer'


def test_filter_jobs_by_location():
    data_to_filter = setup_test_filter_data()
    filtered_jobs = list_window.JobsListWindow.filter_jobs_by_location(data_to_filter, 'Boston')
    assert len(filtered_jobs) == 1  # Expecting 1 job in Boston


def test_filter_remote_jobs():
    data_to_filter = setup_test_filter_data()
    filtered_jobs = list_window.JobsListWindow.filter_remote_jobs(data_to_filter)
    assert len(filtered_jobs) == 1  # Expecting 1 remote job


def test_filter_jobs_by_salary():
    data_to_filter = setup_test_filter_data()
    filtered_jobs = list_window.JobsListWindow.filter_jobs_by_salary(data_to_filter, 85000)
    assert len(filtered_jobs) == 2  # Expecting 2 jobs with salary >= 85000
