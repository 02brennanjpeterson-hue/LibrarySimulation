from contextlib import closing

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import Book, Library


app = FastAPI(title="Library API", version="1.0.0")


class BookRequest(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    pages: int = Field(gt=0)


def book_response(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "pages": book.pages,
        "is_available": book.is_available,
    }


def open_library():
    library = Library("My Library")
    library.seed_if_needed()
    return library


@app.get("/")
def root():
    return {"message": "Library API is running"}


@app.get("/books")
def list_books():
    with closing(open_library()) as library:
        return [book_response(book) for book in library.books]


@app.post("/books", status_code=201)
def add_book(request: BookRequest):
    with closing(open_library()) as library:
        book = Book(request.title, request.author, request.pages)
        library.add_book(book)
        return book_response(book)


@app.post("/books/{title}/borrow")
def borrow_book(title: str):
    with closing(open_library()) as library:
        if library.find_book(title) is None:
            raise HTTPException(status_code=404, detail="Book not found")
        if not library.borrow_book(title):
            raise HTTPException(status_code=409, detail="Book is already borrowed")
        return {"message": "Book borrowed"}


@app.post("/books/{title}/return")
def return_book(title: str):
    with closing(open_library()) as library:
        if library.find_book(title) is None:
            raise HTTPException(status_code=404, detail="Book not found")
        if not library.return_book(title):
            raise HTTPException(status_code=409, detail="Book is already available")
        return {"message": "Book returned"}


@app.delete("/books/{title}")
def remove_book(title: str):
    with closing(open_library()) as library:
        if not library.remove_book(title):
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book removed"}
