NewsHub Documentation
=====================

Welcome to the documentation for NewsHub, a Django-based news application.

NewsHub provides a platform for managing and reading news articles. The
application supports different user roles and includes article management,
newsletters, subscriptions, publishers, and REST API functionality.

Documentation Structure
-----------------------

The documentation is divided into separate sections so that information can
be located easily.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   configuration

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user_guide/index

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   developer_guide/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

Project Overview
----------------

User Roles
~~~~~~~~~~

NewsHub supports four user roles:

* Reader
* Editor
* Journalist
* Publisher

Main Features
~~~~~~~~~~~~~

* User registration and authentication
* Role-based access
* Article creation and management
* Article review and approval
* Newsletters
* Publisher management
* Journalist subscriptions
* REST API functionality
* MariaDB/MySQL database support
* Docker support

Database
~~~~~~~~

NewsHub uses MariaDB/MySQL. Database connection details are configured using
environment variables rather than storing database passwords directly in the
source code.

Docker
~~~~~~

The project includes Docker support using Dockerfile and Docker Compose.
Docker Compose starts the Django web application and MariaDB database.

Testing
~~~~~~~

The Django test suite can be run with:

.. code-block:: powershell

   docker compose exec web python manage.py test news

Application checks can be run with:

.. code-block:: powershell

   docker compose exec web python manage.py check