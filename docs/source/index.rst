.. togglwrapper documentation master file, created by
   sphinx-quickstart on Mon Mar 29 20:53:15 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to togglwrapper's documentation!
========================================

Release v\ |version|. (:ref:`Installation <install>`)

togglwrapper is a `Python <https://www.python.org/>`_ library to easily talk to `Toggl's <https://www.toggl.com>`_ `Track API <https://github.com/toggl/toggl_api_docs>`_. Toggl Track is a free time tracking tool.

Works in Python 2.7+ and Python 3+.

Please see `Toggl's Track API Documentation <https://github.com/toggl/toggl_api_docs>`_ for information about which keys and values to send for the ``data`` dict used during creating and updating.


Features
--------
- Handles authentication for you: only need to provide your API token once
- The most complete Python wrapper: implements all of v8 API.
- Convenient install from PyPI
- Easy to make requests to custom URLs
- Python2 and Python3 compatible
- Uses `requests <http://www.python-requests.org/en/latest/>`_ for seamless HTTP requests


Guides
------

.. toctree::
  :maxdepth: 2

  install
  quickstart


API Documentation
-----------------

.. toctree::
  :maxdepth: 2

  api


Reference
---------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
