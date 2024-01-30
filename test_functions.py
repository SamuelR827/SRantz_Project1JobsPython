""" This is a testing module to test for how the output will write to the file. I will include
more unit tests as the project is expanded more."""
from io import StringIO

from util_functions import write_file_header


def test_write_page_header():
    # Test case to make sure header prints
    file = StringIO()
    write_file_header('Software Engineer', 'New York', file)
    file.seek(0)
    content = file.read()
    assert 'Generated output for Software Engineer near New York.' in content
