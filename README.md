# Library Simulation

Library Simulation is a Python application for managing a small library. It
stores books in a SQLite database and provides two ways to use the application:

- A command-line interface in `main.py`
- A web API built with FastAPI in `api.py`

Both interfaces use the same `Book` and `Library` classes, so changes made
through the CLI or API are saved to the same database.

## Features

- Add books with a title, author, and page count
- List books and show whether each book is available or borrowed
- Borrow available books
- Return borrowed books
- Remove books
- Search for books by title without case sensitivity
- Automatically create the database tables when the application starts
- Add starter books the first time the library is initialized
- Validate API input and return useful HTTP status codes

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Book and library logic, SQLite storage, and CLI menu |
| `api.py` | FastAPI application and HTTP endpoints |
| `requirements.txt` | FastAPI and Uvicorn dependencies |
| `library.db` | Local SQLite database created at runtime |
| `.gitignore` | Excludes the virtual environment, cache files, and local database |

## How the application works

`main.py` defines a `Book` object and a `Library` object. The `Library` object
opens `library.db`, creates the `books` and `settings` tables if necessary, and
loads saved books into memory.

When a book is added, borrowed, returned, or removed, the corresponding SQLite
record is updated and committed. The database is local to the project and is
ignored by Git, so each environment can maintain its own library data.

## Running the command-line application

From the project directory, run:

```powershell
.\.venv\Scripts\python.exe main.py
```

Use the numbered menu to list, add, borrow, return, or remove books. Choose
option `6` to exit.

## Running the API

Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the development server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

The API runs at:

`http://127.0.0.1:8000`

FastAPI provides interactive documentation at:

`http://127.0.0.1:8000/docs`

Use the **Try it out** button in the documentation to send requests from a
browser.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Confirm that the API is running |
| GET | `/books` | Return all books as JSON |
| POST | `/books` | Add a new book |
| POST | `/books/{title}/borrow` | Borrow a book by title |
| POST | `/books/{title}/return` | Return a book by title |
| DELETE | `/books/{title}` | Remove a book by title |

To add a book, send JSON like this to `POST /books`:

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "pages": 412
}
```

Book titles and authors are required, and the page count must be greater than
zero. Successful book creation returns HTTP `201`. Missing books return `404`,
invalid state changes return `409`, and invalid request data returns `422`.

## Technology

- Python
- SQLite
- FastAPI
- Uvicorn
- Pydantic

## Development notes

The API opens and closes a library connection for each request, allowing the
CLI and API to use the same SQLite database safely during local development.
The `--reload` option is intended for development and automatically restarts
the server when Python files change.
