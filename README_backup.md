# NewsHub

NewsHub is a Django-based news application that provides a platform for reading, creating, reviewing, approving and publishing news content.

The application supports different user roles, article management, newsletters, publishers, subscriptions, REST API functionality, MariaDB/MySQL database storage, Docker deployment and Sphinx documentation.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Main Features](#main-features)
* [User Roles](#user-roles)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Documentation](#documentation)
* [Manual Installation](#manual-installation)
* [Docker Installation](#docker-installation)
* [Environment Variables](#environment-variables)
* [Database](#database)
* [Email Configuration](#email-configuration)
* [Running Tests](#running-tests)
* [Django System Checks](#django-system-checks)
* [REST API](#rest-api)
* [Stopping the Application](#stopping-the-application)
* [Taking the Application Live](#taking-the-application-live)
* [Troubleshooting](#troubleshooting)

---

# Project Overview

NewsHub is a Django web application designed to manage and publish news content.

The application provides functionality for:

* User registration and authentication
* Role-based access
* News article creation and management
* Article review and approval
* Publisher management
* Newsletter functionality
* Journalist subscriptions
* REST API access
* MariaDB/MySQL database storage
* Docker-based deployment
* Sphinx software documentation

---

# Main Features

## User Management

Users can register, log in and access functionality based on their assigned role.

NewsHub uses the following roles:

* Reader
* Editor
* Journalist
* Publisher

Role-based permissions determine which parts of the application each user can access.

## Articles

Journalists can create and manage news articles.

Articles can be reviewed and approved before being made available for publication.

## Newsletters

Users can subscribe to newsletter content.

Newsletter functionality allows NewsHub to provide news content to subscribed users.

## Publishers

Publishers can be created and managed within the application.

Articles can be associated with publishers.

## Subscriptions

Readers can subscribe to journalists and access content associated with their subscriptions.

## REST API

NewsHub uses Django REST Framework to provide API functionality.

The project includes API functionality for approved articles and subscribed article content, with permissions controlling access to protected operations.

---

# User Roles

| Role       | General Responsibility                     |
| ---------- | ------------------------------------------ |
| Reader     | Read news content and manage subscriptions |
| Editor     | Review and manage articles                 |
| Journalist | Create and manage news articles            |
| Publisher  | Manage publishing-related functionality    |

Access to specific functionality is controlled by the application's authentication and permission system.

---

# Technology Stack

* Python 3.14
* Django 6.1
* Django REST Framework 3.18.0
* MariaDB 12.3
* MySQL client
* Pillow
* python-dotenv
* Sphinx 9.1.0
* Sphinx Read the Docs theme 3.1.0
* Docker
* Docker Compose

---

# Project Structure

The main project structure is organised as follows:

```text
news_project/
|
+-- docs/
|   +-- _build/
|   |   +-- html/
|   +-- _static/
|   +-- _templates/
|   +-- user_guide/
|   |   +-- articles.rst
|   |   +-- publishers.rst
|   |   +-- newsletters.rst
|   |   +-- subscriptions.rst
|   |   +-- ...
|   +-- conf.py
|   +-- index.rst
|
+-- news/
|   +-- management/
|   |   +-- commands/
|   |       +-- setup_groups.py
|   +-- migrations/
|   +-- templates/
|   +-- models.py
|   +-- forms.py
|   +-- views.py
|   +-- serializers.py
|   +-- permissions.py
|   +-- urls.py
|   +-- ...
|
+-- news_project/
|   +-- settings.py
|   +-- urls.py
|   +-- asgi.py
|   +-- wsgi.py
|
+-- .env
+-- .gitignore
+-- compose.yaml
+-- Dockerfile
+-- manage.py
+-- README.md
+-- requirements.txt
```

The `docs/` directory contains the Sphinx documentation, while the `news/` directory contains the main Django application.

---

# Documentation

NewsHub includes Sphinx-generated software documentation.

The documentation is organised into multiple pages rather than being contained in one large static page.

The generated documentation provides:

* Navigation between sections
* A documentation tree/sidebar
* Search functionality
* Module documentation
* User guides
* API-related documentation
* Links between documentation sections

## Building the Documentation

Activate the project virtual environment first:

```powershell
.\django_env\Scripts\Activate.ps1
```

Install the project requirements:

```powershell
python -m pip install -r requirements.txt
```

Build the documentation:

```powershell
python -m sphinx -b html docs docs/_build/html
```

The generated documentation will be located at:

```text
docs/_build/html/
```

To open the documentation in Microsoft Edge or the default browser:

```powershell
Start-Process ".\docs\_build\html\index.html"
```

## Cleaning the Documentation Build

To remove the previous Sphinx build:

```powershell
python -m sphinx -M clean docs docs/_build
```

Then rebuild it:

```powershell
python -m sphinx -b html docs docs/_build/html
```

---

# Manual Installation

The following instructions provide a complete standalone installation using Python and MariaDB/MySQL.

## 1. Clone the Repository

Clone the project repository:

```powershell
git clone https://github.com/Ralstie/news_project.git
```

Enter the project directory:

```powershell
cd news_project
```

All remaining manual installation commands should be run from the project root.

---

## 2. Create a Virtual Environment

Create the virtual environment inside the project directory:

```powershell
python -m venv django_env
```

Activate it:

```powershell
.\django_env\Scripts\Activate.ps1
```

After activation, PowerShell should show:

```text
(django_env)
```

---

## 3. Install the Requirements

Install all Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

This installs Django, Django REST Framework, the database client, Sphinx and the other dependencies required by NewsHub.

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

The required Django and database variables are:

```text
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=news_project
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

Do not commit real passwords, secret keys or other sensitive credentials to Git.

---

## 5. Create the Database

Create the MariaDB/MySQL database specified by `DB_NAME`.

For example:

```sql
CREATE DATABASE news_project;
```

Create or use a database user with permission to access the database.

For example:

```sql
CREATE USER 'newshub'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON news_project.* TO 'newshub'@'localhost';
FLUSH PRIVILEGES;
```

Make sure the MariaDB/MySQL server is running before starting Django.

---

## 6. Check the Django Configuration

Run:

```powershell
python manage.py check
```

The expected result is:

```text
System check identified no issues (0 silenced).
```

---

## 7. Run Database Migrations

Run:

```powershell
python manage.py migrate
```

---

## 8. Create the User Groups

Run:

```powershell
python manage.py setup_groups
```

This creates the groups required by the NewsHub application.

---

## 9. Start the Development Server

Run:

```powershell
python manage.py runserver
```

Open the application in a browser:

```text
http://127.0.0.1:8000/
```

---

# Docker Installation

Docker provides a separate installation method from the manual Python setup.

The Docker instructions below are intended to be followed independently of the manual installation instructions.

## Requirements

Before starting the Docker setup:

1. Install Docker Desktop.
2. Start Docker Desktop.
3. Make sure the Docker Linux engine is running.
4. Confirm that Docker is available from PowerShell.

Check Docker with:

```powershell
docker info
```

The command should display information about the Docker client and server.

**Docker Desktop must be running when using the Docker commands below.**

---

## 1. Clone the Repository

For a standalone Docker installation, clone the repository:

```powershell
git clone https://github.com/Ralstie/news_project.git
```

Enter the project directory:

```powershell
cd news_project
```

The `Dockerfile` and `compose.yaml` must be available in this directory.

Confirm this with:

```powershell
Get-ChildItem Dockerfile, compose.yaml
```

---

## 2. Build the Docker Image

Build the NewsHub Docker image:

```powershell
docker compose build
```

The Dockerfile performs the following build steps:

1. Starts with the lightweight Python 3.14 image.
2. Creates `/app` as the working directory.
3. Configures Python container behaviour.
4. Installs the system dependencies required by `mysqlclient`.
5. Copies `requirements.txt` into the image.
6. Installs the Python dependencies.
7. Copies the NewsHub source code into the image.
8. Exposes port `8000`.
9. Configures Django to run on port `8000`.

---

## 3. Validate the Compose Configuration

Run:

```powershell
docker compose config
```

This verifies that the Docker Compose configuration can be processed successfully.

---

## 4. Start NewsHub

Start the application and database:

```powershell
docker compose up
```

Docker Compose starts:

* The MariaDB database container
* The NewsHub Django web container

The web container waits for the MariaDB health check to report that the database is ready.

The web container then automatically runs:

```text
python manage.py migrate
python manage.py setup_groups
python manage.py runserver 0.0.0.0:8000
```

The current Docker Compose configuration uses the MariaDB service name `db` as the database hostname inside the Docker network.

---

## 5. Access NewsHub

Once the containers have started successfully, open:

```text
http://127.0.0.1:8000/
```

Alternatively:

```text
http://localhost:8000/
```

---

## 6. Check the Running Containers

Open a second PowerShell window while the application is running.

Enter the project directory:

```powershell
cd news_project
```

Then run:

```powershell
docker compose ps
```

The NewsHub web container and MariaDB database container should be shown as running.

---

## 7. View Docker Logs

To view the web container logs:

```powershell
docker compose logs web
```

To view the MariaDB logs:

```powershell
docker compose logs db
```

To follow the logs while the containers are running:

```powershell
docker compose
```
