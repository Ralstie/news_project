"""Sphinx configuration for the NewsHub project."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "NewsHub"
copyright = "2026, Ralston Lamond"
author = "Ralston Lamond"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]