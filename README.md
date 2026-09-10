# NewsHub

NewsHub is a Django-based news application that allows readers, journalists, editors, and publishers to interact with news content according to their assigned roles.

## Features

* User registration and login.
* Role-based users:

  * Reader
  * Editor
  * Journalist
  * Publisher
* Journalists can create articles.
* Articles can be assigned to publishers.
* Editors can review and approve articles.
* Approved articles can be included in newsletters.
* Publishers can manage publisher information.
* Readers can subscribe to journalists and publishers.
* REST API endpoints are provided for approved articles and subscribed articles.
* Role-based permissions protect API write operations.
* Automated tests are included.

## Technologies

* Python 3.14
* Django 6.1
* Django REST Framework 3.18.0
* MariaDB / MySQL
* mysqlclient
* python-dotenv
* Requests

## Database Setup

NewsHub uses MariaDB/MySQL rather than SQLite.

### 1. Start MariaDB/MySQL

Make sure the MariaDB/MySQL server is running.

### 2. Log in to MySQL

Open PowerShell or Command Prompt and run:

```text
mysql -u root -p
```

Enter the MySQL/MariaDB root password when prompted.

### 3. Create the database

Run the following SQL query:

```sql
CREATE DATABASE news_project
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then exit MySQL:

```sql
EXIT;
```

### 4. Configure environment variables

Create a `.env` file in the project root.

The `.env` file should contain the database connection settings:

```text
DB_NAME=news_project
DB_USER=root
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Replace `your_database_password` with the password for the MySQL/MariaDB user.

The `.env` file is excluded from Git using `.gitignore` and should not be committed because it contains database credentials.

## Installing Dependencies

Create and activate the virtual environment:

```powershell
python -m venv django_env
.\django_env\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## Database Migrations

After configuring the database, run:

```powershell
python manage.py migrate
```

Create the application groups with:

```powershell
python manage.py setup_groups
```

## Running the Application

Start the development server:

```powershell
python manage.py runserver
```

The application can then be accessed at:

```text
http://127.0.0.1:8000/
```

## Running Tests

Run the automated test suite with:

```powershell
python manage.py test
```

The project includes tests covering the main application functionality and permissions.

## Checking the Project

Django's system checks can be run with:

```powershell
python manage.py check
```

To check that migrations are up to date without creating new migration files:

```powershell
python manage.py makemigrations --check --dry-run
```

## Project Structure

```text
news_project/
│
├── manage.py
├── .env
├── .gitignore
│
├── news/
│   ├── migrations/
│   ├── management/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── news_project/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## Security Notes

Database credentials are stored in environment variables rather than directly in the Django settings file.

The `.env` file is ignored by Git and must not be uploaded to the repository.

For production deployment, the Django secret key, debug setting, allowed hosts, and email/database credentials should also be configured through secure environment variables.
