from serpAPI import perform_search
from util_functions import write_page_to_file


def main():
    json_data = perform_search()
    write_page_to_file(json_data, "results.txt")


main()
