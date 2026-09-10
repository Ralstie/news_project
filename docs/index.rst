NewsHub Documentation
=====================

Welcome to the documentation for NewsHub, a Django-based news application.

Overview
========

NewsHub is a Django web application that provides a platform for managing
and reading news articles.

The application supports four user roles:

* Reader
* Editor
* Journalist
* Publisher

Main Features
=============

User Management
---------------

Users can register and log into the NewsHub application. User roles determine
which features and dashboards are available to them.

Articles
--------

Journalists can create and manage news articles. Articles can be reviewed and
approved before publication.

Newsletters
-----------

The application provides newsletter functionality for users who subscribe to
news content.

Publishers
----------

Publishers can be created and managed through the application and can be
associated with articles.

Subscriptions
-------------

Readers can subscribe to journalists and access subscribed content through
the subscriptions functionality.

REST API
--------

NewsHub includes REST API endpoints built using Django REST Framework.

The API provides functionality related to articles and approved articles,
with permissions controlling access to write operations.

Database
========

NewsHub uses MariaDB/MySQL as its database.

The database connection is configured through environment variables rather
than storing database passwords directly in the source code.

Docker
======

The project includes Docker support using:

* ``Dockerfile``
* ``compose.yaml``
* MariaDB

The Docker Compose configuration starts both the Django web application and
the MariaDB database.

Testing
=======

The Django test suite can be run using:

.. code-block:: powershell

   docker compose exec web python manage.py test news

The project should report that all tests pass.

Application Checks
==================

Django's system checks can be run using:

.. code-block:: powershell

   docker compose exec web python manage.py check

Documentation
=============

The project documentation is generated using Sphinx.

To build the HTML documentation from the project root:

.. code-block:: powershell

   sphinx-build -b html docs docs/_build/html

The generated documentation can then be viewed by opening
``docs/_build/html/index.html`` in a web browser.