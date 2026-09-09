class Book:
    def __init__(self, title, author, pages):
        # A new book starts as available.
        self.title = title
        self.author = author
        self.pages = pages
        self.is_available = True

    def borrow(self):
        # Return False when the book is already borrowed.
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def return_book(self):
        # Mark the book as available again.
        self.is_available = True

    def __str__(self):
        # This formatted text is shown when the book is listed.
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.title} by {self.author} ({self.pages} pages) - {status}"


class Library:
    def __init__(self, name):
        self.name = name
        # The library stores each Book object in this list.
        self.books = []

    def add_book(self, book):
        # Keep the whole object so its availability can change later.
        self.books.append(book)

    def find_book(self, title):
        # Compare lowercase titles to make the search case-insensitive.
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        # None signals that no matching book was found.
        return None

    def list_books(self):
        # Handle an empty library before looping through the books.
        if not self.books:
            print("The library has no books.")
            return

        # enumerate provides the user-friendly numbers shown in the menu.
        for number, book in enumerate(self.books, start=1):
            print(f"{number}. {book}")

    def remove_book(self, title):
        # Reuse find_book so removal uses the same case-insensitive search.
        book = self.find_book(title)
        if book is None:
            return False
        self.books.remove(book)
        return True


def seed_library():
    # Build the starting library with a couple of example books.
    library = Library("My Library")
    library.add_book(Book("Little Book", "Bob Murray", 350))
    library.add_book(Book("Big Book", "DJT", 1000))
    return library


def run():
    # Keep displaying the menu until the user selects Exit.
    library = seed_library()

    while True:
        # The menu is printed again after each completed action.
        print(f"\n{library.name}")
        print("1. List books")
        print("2. Add book")
        print("3. Borrow book")
        print("4. Return book")
        print("5. Remove book")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Show every book and its current availability.
            library.list_books()
        elif choice == "2":
            # Collect the new book's details before adding it.
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            pages = int(input("Number of pages: "))
            library.add_book(Book(title, author, pages))
            print("Book added.")
        elif choice == "3":
            # Find the book, then try to change it from available to borrowed.
            book = library.find_book(input("Title to borrow: ").strip())
            if book is None:
                print("Book not found.")
            elif book.borrow():
                print("Book borrowed.")
            else:
                print("That book is already borrowed.")
        elif choice == "4":
            # Find the book and mark it as available again.
            book = library.find_book(input("Title to return: ").strip())
            if book is None:
                print("Book not found.")
            else:
                book.return_book()
                print("Book returned.")
        elif choice == "5":
            # Remove the matching Book object from the library list.
            title = input("Title to remove: ").strip()
            if library.remove_book(title):
                print("Book removed.")
            else:
                print("Book not found.")
        elif choice == "6":
            # break exits the loop and ends the interactive program.
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    run()
