"""Sphinx configuration."""
project = "atomic-operator-runner"
author = "Josh Rickard"
copyright = "2022, Swimlane"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
