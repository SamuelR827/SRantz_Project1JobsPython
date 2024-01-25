from serpAPI import perform_search

num_pages = 5


def main():
    file = open("results.txt", "w")
    perform_search(num_pages, file)
    file.close()


main()
