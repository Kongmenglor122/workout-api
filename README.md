# Workout API

## Project Structure

| Path | Responsibility |
| --- | --- |
| `app/main.py` | Create the FastAPI app and register routers |
| `app/database.py` | Configure the database engine, sessions, and `get_db` |
| `app/models.py` | Define SQLAlchemy database tables |
| `app/schemas.py` | Define Pydantic request and response schemas |
| `app/routers/machines.py` | Define machine CRUD endpoints |
| `app/__init__.py` | Mark `app` as a Python package |
| `app/routers/__init__.py` | Mark `routers` as a Python package |
| `.env` | Store local database credentials; ignored by Git |
| `.env.example` | Document required settings using placeholder values |
| `requirements.txt` | Record project dependencies |
| `.gitignore` | Specify files Git should ignore |
| `README.md` | Explain the project and how to run it |

## Understanding the Files

- **Models:** What does the database store?
- **Schemas:** What data can the API accept and return?
- **Routers:** What happens when someone calls an endpoint?

## Install Dependencies

With your virtual environment activated, install all packages listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt

## Run the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the development server from the project root:

```bash
python -m uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/
- Interactive documentation: http://127.0.0.1:8000/docs
- `--reload` restarts the server when code changes.
- Press `Control+C` to stop the server.

## Models, Schemas, and Routers

| File | Responsibility | Example |
| --- | --- | --- |
| `app/models.py` | Define database tables using SQLAlchemy | A machine has an ID, name, muscle group, and description |
| `app/schemas.py` | Define and validate API request and response data using Pydantic | Creating a machine requires a name and muscle group |
| `app/routers/machines.py` | Handle HTTP requests and return responses | `POST /machines` creates a machine |

### Models: What does the database store?

SQLAlchemy models describe database tables and their columns.

```python
class Machine(Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
```

- `Mapped[int]` describes a mapped Python attribute holding an integer.
- `mapped_column()` configures the database column.
- `primary_key=True` makes the column the unique identifier for each row.
- `String(100)` sets a database string length limit of 100 characters.

Defining a model does not create the table automatically. Python must import
the model before `Base.metadata.create_all(bind=engine)` runs.

`create_all()` creates missing tables. It does not update existing table
structures; we will use migrations for those changes.

### Schemas: What data does the API accept and return?

Pydantic schemas define and validate request and response data.

```python
class MachineCreate(BaseModel):
    name: str
    muscle_group: str
    description: str | None = None
```

This request schema requires `name` and `muscle_group`. The description can
be omitted or set to null. The client does not supply an ID because the
database generates it.

Schemas do not create database tables.

### Routers: What happens when someone calls an endpoint?

Routers connect HTTP methods and URLs to Python functions.

For example, a `POST /machines` endpoint:
1. Receives data validated against a Pydantic schema.
2. Creates a SQLAlchemy model object.
3. Saves it using a database session.
4. Returns a response.

### Why separate these files?

The database structure, API validation, and request handling have different
responsibilities. Keeping them separate makes the code easier to understand
and maintain.

The filenames are conventions, not requirements. A model can live in
`machine.py`, but that file must be imported for SQLAlchemy to register it.

Remember: Models describe storage, schemas validate data, and routers handle requests.
