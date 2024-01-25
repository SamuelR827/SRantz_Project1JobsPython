import json

line_seperator = "\n" + ("-" * 256) + "\n"


def write_page_header(query, location, file):
    page_header = f"Generated output for {query} in {location}.\n"
    file.write(page_header)


def write_page_to_file(json_data, page, file):
    page_number_to_write = "Page " + str(page) + "\n"
    lines_to_write = json.dumps(json_data, indent=4)
    file.write(page_number_to_write)
    file.write(lines_to_write)
    file.write(line_seperator)
