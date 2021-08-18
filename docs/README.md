# Documentation

📖 Read the live docs at [togglwrapper.readthedocs.io](https://togglwrapper.readthedocs.io/en/latest/)

We use [Sphinx](https://www.sphinx-doc.org) to generate togglwrapper's documentation.

- [Sphinx Quickstart](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
- [Autodoc extention documentation](https://www.sphinx-doc.org/en/master/usage/quickstart.html#autodoc)

## Generating Docs

(Assuming virtualenvwrapper is used for virtual environments.)

```
mkvirtualenv twdocs
pip install -r docs/requirements.txt
cd docs/
make html
```

## Tour

- Raw source files live in the `/source` folder.

- The "compiled" docs that `make html` generates lives in the `/build` folder.

- Configurations for Sphinx are in `source/conf.py`.
  This is where you can enable or disable plugins, themes, etc.

## Troubleshooting

```
WARNING: Could not lex literal_block as "python". Highlighting skipped.
```
Means that the code block it's complaining about isn't valid Python. Frustratingly doesn't tell you
which line. You'll have to go digging for the mistake.

```
WARNING: autodoc: failed to import class 'Toggl' from module 'togglwrapper'; the following exception was raised:
No module named 'togglwrapper'
```
Ensure you have the virtualenv active and have the `docs/requirements` installed.
You can use `pip freeze` to inspect what's currently installed.

If you made changes to the docstrings and want to see them reflected, you'll have to install a local version of togglwrapper instead of installing from pypi. To install your local in-progress togglwrapper:

1. Update `togglwrapper/__init__.py` to have an alpha version of the next minor or major release. e.g. `__version__ = '2.0.1-alpha'`
2. `pip install -e .` (while standing in the root directory, not `/docs`)

```
docstring of <path>:<line>: WARNING: Unexpected indentation.
```
Means it's missing a newline.
