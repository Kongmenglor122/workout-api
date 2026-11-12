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
