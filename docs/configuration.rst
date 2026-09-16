Configuration
=============

NewsHub uses environment variables for configuration values that should not
be stored directly in the source code.

Database Configuration
----------------------

The database settings use the following environment variables:

.. code-block:: text

   DB_NAME
   DB_USER
   DB_PASSWORD
   DB_HOST
   DB_PORT

The values should be configured for the local MariaDB/MySQL installation.

Security
--------

Database passwords and other credentials should not be committed to the
Git repository.

Email Configuration
-------------------

During development, NewsHub can use Django's console email backend.

For a live deployment, an SMTP email provider should be configured in
``news_project/settings.py``.

The live SMTP configuration should contain values such as:

.. code-block:: python

   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_HOST = "smtp.example.com"
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = "your-email@example.com"
   EMAIL_HOST_PASSWORD = "your-email-password"
   DEFAULT_FROM_EMAIL = "your-email@example.com"

Do not commit real email passwords or other secrets to the repository.

Live Environment
----------------

Before deploying NewsHub to a live environment:

* Configure a production database.
* Configure a live SMTP email provider.
* Set secure database credentials.
* Set secure email credentials.
* Configure the appropriate allowed hosts.
* Review Django's production security settings.