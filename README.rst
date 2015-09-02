=============
Toggl Wrapper
=============

Python library to easily interface with Toggl's API.

Only supports the main Toggl API, not the Reports API (coming soon).

Works in Python 2.7+ and Python 3+


-----
Toggl
-----

`Toggl <https://www.toggl.com>`_ is free time tracking software.


-------
Install
-------

.. code-block:: bash

    $ pip install togglwrapper


----------
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
    u'name': u"Your workspace",
    ...
    }]
    >>> toggl.Clients.create({"client":{"name":"Very Big Company", "wid": 1234}})
    {u'data': {u'id': 294021, u'name': u'Very Big Company', u'wid': 1234}}


-------------------
Documentation
-------------------
Find the full documentation `here <http://togglwrapper.readthedocs.org/en/latest/>`_.

---------------------------
API Endpoints Documentation
---------------------------

For full details on what fields are required, and what endpoints are available, see the `Toggl API docs <https://github.com/toggl/toggl_api_docs>`_
