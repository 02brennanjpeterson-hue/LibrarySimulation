# Library Simulation

This project is a library management application backed by SQLite. It includes
both a command-line interface and a FastAPI web API.

## API overview

The API is defined in `api.py` and uses the `Library` class from `main.py`.
Book data is stored in `library.db`.

Supported operations:

- List all books
- Add a book
- Borrow a book
- Return a book
- Remove a book

FastAPI validates incoming book data, including required titles and authors and
positive page counts. The API returns book data as JSON.

## Running the API

Install the dependencies from the project directory:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Interactive Swagger documentation is available at:

`http://127.0.0.1:8000/docs`

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/books` | List books |
| POST | `/books` | Add a book |
| POST | `/books/{title}/borrow` | Borrow a book |
| POST | `/books/{title}/return` | Return a book |
| DELETE | `/books/{title}` | Remove a book |

The API was added in commit `d44be01`.
