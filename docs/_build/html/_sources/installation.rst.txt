Installation
============

This page explains how to install and run NewsHub manually.

Prerequisites
-------------

The following software is required:

* Python
* MariaDB/MySQL
* Git

Clone the Project
-----------------

Clone the repository and enter the project directory:

.. code-block:: powershell

   git clone https://github.com/Ralstie/news_project.git
   cd news_project

Create a Virtual Environment
----------------------------

Create a virtual environment inside the project directory:

.. code-block:: powershell

   python -m venv venv

Activate the virtual environment:

.. code-block:: powershell

   .\venv\Scripts\Activate.ps1

Install Dependencies
--------------------

Install the packages listed in ``requirements.txt``:

.. code-block:: powershell

   python -m pip install -r requirements.txt

Database Setup
--------------

Create the MariaDB/MySQL database required by NewsHub.

The database configuration is supplied through environment variables. Refer
to the :doc:`configuration` page for the required settings.

Run Migrations
--------------

Apply the Django database migrations:

.. code-block:: powershell

   python manage.py migrate

Create a Superuser
------------------

Create an administrator account if required:

.. code-block:: powershell

   python manage.py createsuperuser

Set Up User Groups
------------------

Run the NewsHub management command:

.. code-block:: powershell

   python manage.py setup_groups

Run the Development Server
--------------------------

Start the Django development server:

.. code-block:: powershell

   python manage.py runserver

The application can then be accessed through the local development server.