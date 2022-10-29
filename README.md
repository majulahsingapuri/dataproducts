# dataprod

## Prerequisites

* Python 3.9+
* [Poetry](https://python-poetry.org/docs/)
* PostgreSQL or Docker
* [Caddy](https://caddyserver.com/v2)

## Setup

0. If using Poetry, run `poetry env use $(pyenv which python)` to ensure Poetry is using the right Python configuration.

1. Install dependencies with Poetry. This will also create a virtual environment at `.venv` if it does not exist yet.

   ```bash
   poetry install
   ```

2. Activate the virtual environment. The command is different depending on your OS and shell.
   Alternatively, `poetry shell` may work, but it might not launch the correct shell.

   | OS                            | Shell                           | Command                          |
   |-------------------------------|---------------------------------|----------------------------------|
   | Windows                       | PowerShell (preferred)          | `.venv/Scripts/Activate.ps1`     |
   | Windows                       | Command Prompt (don't use this) | `.venv/Scripts/activate.bat`     |
   | Windows                       | Unix shell (eg. Git Bash)       | `source .venv/Scripts/activate`  |
   | Unix-like (eg. Ubuntu, macOS) | Unix shell (eg. bash, zsh)      | `source .venv/bin/activate`      |
   | Unix-like                     | fish                            | `source .venv/bin/activate.fish` |

3. Copy the `template.env` file to `.env`, which will be used to configure the application.

   ```bash
   cp template.env .env
   ```

4. Set up the database. Refer to [Database setup](#database-setup) for instructions on setting up the database locally
   or within Docker.

5. Run database migrations.

   ```bash
   python manage.py migrate
   ```

6. Set up pre-commit hooks.

   ```bash
   pre-commit install
   ```

7. Run the test suite with coverage

   ```bash
   pytest --cov
   ```

8. Create a local superuser.

   ```bash
   python manage.py createsuperuser
   ```

9. Start the development server. This will listen on localhost:8000

   ```bash
   python manage.py runserver
   ```

10. Start the frontend server (refer to [dataprod-app](https://github.com/dataprod/dataprod-app)). This will listen on
    localhost:3000

11. Start Caddy in a new terminal to reverse-proxy both the backend and frontend through the same origin to avoid
    session authentication and CORS issues. The application will be accessible at `http://localhost:8080`

      ```bash
      caddy run
      ```

## Database setup

### Option 1: Local PostgreSQL installation

1. Use `psql` to create a new user and database for the application with appropriate permissions:

   ```bash
   echo "create user dataprod login password 'password';
   create database dataprod owner dataprod;
   alter user dataprod createdb;" | psql -d postgres
   ```

### Option 2: Running PostgreSQL in Docker

1. Create a volume to persist the database between container restarts:

   ```bash
   docker volume create dataprod_db
   ```

2. Start the database container:

   ```bash
   docker run -d -v dataprod_db:/var/lib/postgresql/data -e POSTGRES_USER=dataprod -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dataprod -p 5432:5432 --name dataprod_db postgres
   ```
