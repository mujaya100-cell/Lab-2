

import csv
from xml.dom import minidom


# Read all book records from the provided CSV file.
def read_books():
    with open("books.csv", "r", encoding="cp1251", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        books = list(reader)
    return books


# Task 1: Count titles longer than 30 characters.
def count_long_titles(books):
    count = 0

    for book in books:
        title = book["Название"]
        if len(title) > 30:
            count += 1

    print("1. Названий длиннее 30 символов:", count)


# Task 2: Search by author. Variant 5 has no additional restrictions.
def search_by_author(books):
    name = input("\n2. Введите имя или фамилию автора (Enter — пропустить): ")
    name = name.strip().lower()

    if name == "":
        print("Поиск пропущен.")
        return

    count = 0
    for book in books:
        author = book["Автор"]
        full_name = book["Автор (ФИО)"]

        if name in author.lower() or name in full_name.lower():
            count += 1
            print(str(count) + ".", author, "—", book["Название"])

    print("Найдено записей:", count)


# Task 3: Write 20 numbered bibliographic references to a text file.
def create_bibliography(books):
    count = 0
    used_titles = set()

    with open("bibliography.txt", "w", encoding="utf-8") as file:
        for book in books:
            author = book["Автор"].strip()
            title = book["Название"].strip()

            if author == "" or title == "":
                continue

            
            if title in used_titles:
                continue

            
            date = book["Дата поступления"]       
            year = date.split(" ")[0].split(".")[2]

            count += 1
            file.write(f"{count}. {author}. {title} - {year}\n")
            used_titles.add(title)

            if count == 20:
                break

    print("\n3. Библиографических ссылок сохранено:", count)
    print("Файл: bibliography.txt")
    print("Примечание: год взят из даты поступления книги.")


# Task 4: Extract CharCode and Value into two separate lists.
def read_currencies():
    document = minidom.parse("currency.xml")
    currencies = document.getElementsByTagName("Valute")

    char_codes = []
    values = []

    for currency in currencies:
        code = currency.getElementsByTagName("CharCode")[0].firstChild.nodeValue
        value_text = currency.getElementsByTagName("Value")[0].firstChild.nodeValue
        value = float(value_text.replace(",", "."))

        char_codes.append(code)
        values.append(value)

    print("\n4. Два списка из currency.xml:")
    print("CharCode:", char_codes)
    print("Value:", values)

    with open("currency_lists.txt", "w", encoding="utf-8") as file:
        file.write("CharCode = " + str(char_codes) + "\n")
        file.write("Value = " + str(values) + "\n")

    print("Всего валют:", len(char_codes))
    print("Файл: currency_lists.txt")


# Extra task 1: Get all unique tags from the genre column.
def find_unique_tags(books):
    tags = set()

    for book in books:
        genres = book["Жанр книги"]
        for tag in genres.split("#"):
            tag = tag.strip()
            if tag != "":
                tags.add(tag)

    sorted_tags = sorted(tags)

    print("\n5. Все уникальные теги:")
    with open("unique_tags.txt", "w", encoding="utf-8") as file:
        for tag in sorted_tags:
            print(tag)
            file.write(tag + "\n")

    print("Всего тегов:", len(tags))
    print("Файл: unique_tags.txt")


# Used when sorting the books by their borrowing counts.
def get_borrowings(book):
    return book["borrowings"]


# Extra task 2: Find the 20 most popular books.
def find_popular_books(books):
    books_by_id = {}

    for book in books:
        book_id = book["ID"]
        borrowings = int(book["Кол-во выдач"])

        # Several CSV records can have the same book ID.
        if book_id not in books_by_id:
            books_by_id[book_id] = {
                "author": book["Автор"],
                "title": book["Название"],
                "borrowings": 0
            }

        books_by_id[book_id]["borrowings"] += borrowings

    all_books = list(books_by_id.values())
    all_books.sort(key=get_borrowings, reverse=True)
    top_20 = all_books[:20]

    print("\n6. 20 самых популярных книг:")
    with open("top_20_books.txt", "w", encoding="utf-8") as file:
        for number, book in enumerate(top_20, start=1):
            line = (str(number) + ". " + book["author"] + ". "
                    + book["title"] + " — выдач: " + str(book["borrowings"]))
            print(line)
            file.write(line + "\n")

    print("Файл: top_20_books.txt")



def main():
    books = read_books()
    print("Прочитано записей из books.csv:", len(books))

    count_long_titles(books)
    search_by_author(books)
    create_bibliography(books)
    read_currencies()
    find_unique_tags(books)
    find_popular_books(books)


if __name__ == "__main__":
    main()
