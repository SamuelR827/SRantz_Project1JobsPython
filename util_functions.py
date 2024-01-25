import json

line_seperator = ("-" * 256) + "\n"


def write_page_to_file(json_data, filename):
    lines_to_write = json.dumps(json_data, indent=4)
    with open(filename, "w") as file:
        file.write(lines_to_write)
