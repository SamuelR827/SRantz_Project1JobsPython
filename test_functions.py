from io import StringIO

import pytest

from util_functions import write_page_to_file


def test_write_page_header():
    file = StringIO()
    write_page_to_file({'mocked_results': 'data'}, 1, file)

    content = file.read()
    assert '"mocked_results": "data"' in content
    assert '"Page 1"' in content
    assert '-' * 256 in content
