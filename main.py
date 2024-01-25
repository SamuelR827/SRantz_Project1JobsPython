from serpAPI import perform_search


def main():
    filename = "results.txt"
    num_pages = 5
    with open(filename, "w") as file:
        perform_search(num_pages, file)


if __name__ == "__main__":
    main()
