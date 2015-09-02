.. togglwrapper documentation master file, created by
   sphinx-quickstart on Tue Sep  1 10:22:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to togglwrapper's documentation!
========================================

Release v\ |version|. (:ref:`Installation <install>`)

Easily interface with `Toggl's <https://www.toggl.com>`_ API. Toggl is free time tracking software.

Works in Python 2.7+ and Python 3+.

Please see `Toggl's API Documentation <https://github.com/toggl/toggl_api_docs>`_ for information about which keys and values to send for the ``data`` dict used during creating and updating.

Installing:
-----------

.. toctree::
  :maxdepth: 1

  install


Quickstart
----------

.. code-block:: python

    >>> from togglwrapper import Toggl
    >>> toggl = Toggl('your_api_token')``
    >>> toggl.User.get()
    {u'data': {u'achievements_enabled': True,
    u'api_token': u'your_api_token',
    u'email': u'your_email@domain.com',
    u'fullname': u'Your Name',
    ...
    }
    >>> toggl.Clients.get()
    [{u'at': u'2015-07-02T14:27:59+00:00',
    u'id': 12031893,
    u'name': u'Client Name',
    u'wid': 3928}]
    >>> toggl.Workspaces.get()
    [{u'admin': True,
    u'api_token': u'your_api_token',
    u'id': 1234,
    ..
    }]
    >>> toggl.Clients.create({"client":{"name":"Very Big Company", "wid": 1234}})
    {u'data': {u'id': 294021, u'name': u'Very Big Company', u'wid': 1234}}


API Documentation:
------------------

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

