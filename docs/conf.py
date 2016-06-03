#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# flake8: noqa

import desmod

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

autodoc_member_order = 'bysource'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'desmod'
copyright = '2016, Western Digital Corporation'
author = 'Pete Grayson'
version = desmod.__version__
release = desmod.__version__
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'desmoddoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'desmod.tex', 'desmod Documentation',
     'Pete Grayson', 'manual'),
]
man_pages = [
    (master_doc, 'desmod', 'desmod Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'desmod', 'desmod Documentation',
     author, 'desmod', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'simpy': ('https://simpy.readthedocs.io/en/latest/', None)
}
