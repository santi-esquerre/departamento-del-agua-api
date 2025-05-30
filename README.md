# Departamento del Agua

A FastAPI + SQLModel + Alembic + PostgreSQL application for managing academic, blog, and departmental resources.

## Features

- Academic domain: Carreras, Materias, Requisitos
- Blog domain: BlogPost CRUD and search
- Equipamiento, Proyectos, Personal, Publicaciones, Servicios
- Alembic migrations
- Async SQLModel/PostgreSQL
- Pytest-based test suite

## Quickstart

### 1. Clone the repository

```bash
git clone <repo-url>
cd departamento_del_agua
```

### 2. Set up environment variables

Create a `.env` file in the project root with the following (example values):

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/departamento_del_agua
UPLOAD_DIR=./uploads
SECRET_KEY=your-secret-key
# Add other secrets as needed
```

**Note:** Never commit your `.env` or any file with secrets to version control.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Alembic migrations

```bash
alembic upgrade head
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

### 6. Run tests

```bash
pytest
```

## Project Structure

- `app/` - Main application code
- `app/models/` - SQLModel models
- `app/schemas/` - Pydantic schemas
- `app/routes/` - FastAPI routes
- `app/services/` - Business logic/services
- `app/storage/` - File storage logic
- `alembic/` - Database migrations
- `tests/` - Test suite

## Security & Best Practices

- **Never commit secrets or database credentials.**
- Use environment variables for all sensitive configuration.
- See `.gitignore` for patterns to exclude secrets and local files.

## Docker Deployment

You can run the full stack (API + PostgreSQL) using Docker Compose.

### 1. Build and start the containers

```bash
docker-compose up --build
```

This will:

- Start a PostgreSQL database (service: `db`)
- Build and run the FastAPI app (service: `web`)
- Mount your local `app/`, `alembic/`, and `uploads/` directories into the container for live code reload and persistent uploads.

### 2. Environment variables

- The `web` service uses the following environment variables (see `.env.example`):
  - `DATABASE_URL` (should match the connection string for the `db` service)
  - `UPLOAD_DIR` (default: `./uploads`)
  - `SECRET_KEY` (set your own secret)
- You can override/add variables in the `docker-compose.yml` or by using a `.env` file (see Docker Compose docs).

### 3. Database migrations

After the containers are up, run Alembic migrations inside the `web` container:

```bash
docker-compose exec web alembic upgrade head
```

### 4. Accessing the app

- API: [http://localhost:8000](http://localhost:8000)
- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Database: exposed on port 5432 (default user/pass/db: `cenur/cenur_pass/cenur_db`)

### 5. Stopping and cleaning up

```bash
docker-compose down
```

- To remove all data (including database volume):

```bash
docker-compose down -v
```

---

## License

MIT
