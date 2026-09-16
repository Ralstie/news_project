Testing
=======

Run the Django test suite with:

.. code-block:: powershell

   python manage.py test news

When using Docker:

.. code-block:: powershell

   docker compose exec web python manage.py test news

Django System Checks
--------------------

Run Django's system checks with:

.. code-block:: powershell

   python manage.py check

When using Docker:

.. code-block:: powershell

   docker compose exec web python manage.py check