from io import StringIO

from util_functions import write_file_header


def test_write_page_header():
    file = StringIO()
    write_file_header('Software Engineer', 'New York', file)

    file.seek(0)
    content = file.read()
    assert 'Generated output for Software Engineer in New York.' in content
