.. togglwrapper documentation master file, created by
   sphinx-quickstart on Tue Sep  1 10:22:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to togglwrapper's documentation!
========================================

Release v\ |version|. (:ref:`Installation <install>`)

Python library to easily interface with `Toggl's <https://www.toggl.com>`_ API. Toggl is free time tracking software.

Works in Python 2.7+ and Python 3+.

Please see `Toggl's API Documentation <https://github.com/toggl/toggl_api_docs>`_ for information about which keys and values to send for the ``data`` dict used during creating and updating.


Features
--------
- Handles authentication for you: only need to provide your API token once
- The most complete Python wrapper: implements all of v8 API.
- Convenient install from PyPI
- Easy to make requests to custom URLs
- Python2 and Python3 compatible
- Uses `requests <http://www.python-requests.org/en/latest/>`_ for seamless HTTP requests


Guide
-----

.. toctree::
  :maxdepth: 2

  install
  quickstart


API Documentation
-----------------

.. toctree::
  :maxdepth: 2

  api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

