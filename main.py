import sqlite3
from pathlib import Path


class Book:
    def __init__(self, title, author, pages, is_available=True, book_id=None):
        # A new book starts as available.
        self.id = book_id
        self.title = title
        self.author = author
        self.pages = pages
        self.is_available = is_available

    def borrow(self):
        # Return False when the book is already borrowed.
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def return_book(self):
        # Return False when the book is already available.
        if self.is_available:
            return False
        self.is_available = True
        return True

    def __str__(self):
        # This formatted text is shown when the book is listed.
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.title} by {self.author} ({self.pages} pages) - {status}"


class Library:
    def __init__(self, name, database_path=None):
        self.name = name
        self.database_path = Path(database_path or Path(__file__).with_name("library.db"))
        self.connection = self._open_database()
        self.books = []
        self._initialize_database()
        self._load_books()

    def _open_database(self):
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA schema_version").fetchone()
        except sqlite3.DatabaseError:
            connection.close()
            backup_path = self.database_path.with_suffix(
                self.database_path.suffix + ".corrupt"
            )
            suffix = 1
            while backup_path.exists():
                backup_path = self.database_path.with_suffix(
                    self.database_path.suffix + f".corrupt.{suffix}"
                )
                suffix += 1
            self.database_path.replace(backup_path)
            print(
                f"Database was invalid; the original was saved as {backup_path.name}."
            )
            connection = sqlite3.connect(self.database_path)
        return connection

    def _initialize_database(self):
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                pages INTEGER NOT NULL,
                is_available INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def _load_books(self):
        rows = self.connection.execute(
            "SELECT id, title, author, pages, is_available "
            "FROM books ORDER BY id"
        ).fetchall()
        self.books = [
            Book(
                title,
                author,
                pages,
                bool(is_available),
                book_id,
            )
            for book_id, title, author, pages, is_available in rows
        ]

    def seed_if_needed(self):
        seeded = self.connection.execute(
            "SELECT value FROM settings WHERE name = 'seeded'"
        ).fetchone()
        if seeded is not None:
            return

        self.add_book(Book("Little Book", "Bob Murray", 350))
        self.add_book(Book("Big Book", "DJT", 1000))
        self.connection.execute(
            "INSERT INTO settings (name, value) VALUES ('seeded', 'true')"
        )
        self.connection.commit()

    def close(self):
        self.connection.close()

    def add_book(self, book):
        cursor = self.connection.execute(
            "INSERT INTO books (title, author, pages, is_available) "
            "VALUES (?, ?, ?, ?)",
            (book.title, book.author, book.pages, int(book.is_available)),
        )
        book.id = cursor.lastrowid
        self.books.append(book)
        self.connection.commit()

    def find_book(self, title):
        # Compare normalized titles to make the search case-insensitive.
        normalized_title = title.strip().lower()
        for book in self.books:
            if book.title.strip().lower() == normalized_title:
                return book
        # None signals that no matching book was found.
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book is None or not book.borrow():
            return False
        self.connection.execute(
            "UPDATE books SET is_available = 0 WHERE id = ?", (book.id,)
        )
        self.connection.commit()
        return True

    def return_book(self, title):
        book = self.find_book(title)
        if book is None or not book.return_book():
            return False
        self.connection.execute(
            "UPDATE books SET is_available = 1 WHERE id = ?", (book.id,)
        )
        self.connection.commit()
        return True

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
        self.connection.execute("DELETE FROM books WHERE id = ?", (book.id,))
        self.books.remove(book)
        self.connection.commit()
        return True


def seed_library():
    library = Library("My Library")
    library.seed_if_needed()
    return library


def run():
    # Keep displaying the menu until the user selects Exit.
    library = seed_library()

    try:
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
                library.list_books()
            elif choice == "2":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                pages = int(input("Number of pages: "))
                library.add_book(Book(title, author, pages))
                print("Book added.")
            elif choice == "3":
                title = input("Title to borrow: ").strip()
                book = library.find_book(title)
                if book is None:
                    print("Book not found.")
                elif library.borrow_book(title):
                    print("Book borrowed.")
                else:
                    print("That book is already borrowed.")
            elif choice == "4":
                title = input("Title to return: ").strip()
                book = library.find_book(title)
                if book is None:
                    print("Book not found.")
                elif library.return_book(title):
                    print("Book returned.")
                else:
                    print("That book is already available.")
            elif choice == "5":
                title = input("Title to remove: ").strip()
                if library.remove_book(title):
                    print("Book removed.")
                else:
                    print("Book not found.")
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Please choose a number from 1 to 6.")
    finally:
        library.close()


if __name__ == "__main__":
    run()
