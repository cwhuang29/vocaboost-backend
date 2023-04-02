# vocabulary-highlighter-backend

Backend server for browser extension and app of vocabulary-highlighter.

## Commands

- Run the server: `uvicorn main:app --reload`
    - See API documents at `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/redoc`

## Setup

1. Setup python environment

    ```bash
    pip3 install virtualenv
    python3 -m virtualenv venv
    source venv/bin/activate
    pip install fastapi "uvicorn[standard]" SQLAlchemy pymysql email-validator
    ```

2. Check `config.py` and setup all necessary env variables

## Structure

- `routers/`: routers of the backend apis
- `handlers/`: handlers for incoming network requests
- `structs/`
    - `requests/`: format of network requests’ body
    - `models/`: ORM classes (interact with the database)
    - `schemas/`: data validation, conversion, and documentation classes. Defines more or less a "schema" (a valid data shape)

    Note: **SQLAlchemy** uses the term "**model**" to refer to these classes and instances that interact with the database. **Pydantic** also uses the term "**model**" (refer to **schema** here) to refer to something different, the data validation, conversion, and documentation classes and instances.

- `databases/`: interact with the data in the database
- `utils/`: utilities and helper functions
