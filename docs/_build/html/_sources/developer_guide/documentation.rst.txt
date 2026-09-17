Building the Documentation
===========================

Sphinx is used to generate the NewsHub documentation.

Install Sphinx if necessary:

.. code-block:: powershell

   python -m pip install sphinx sphinx-rtd-theme

Build the HTML documentation:

.. code-block:: powershell

   python -m sphinx -b html docs docs/_build/html

The generated documentation is stored in:

.. code-block:: text

   docs/_build/html/