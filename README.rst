=============
Toggl Wrapper
=============

Python library to easily interface with Toggl's API.

Implements all of Toggl's main API. The Reports API is not yet supported (coming soon).

Works in Python 2.7+ and Python 3+, and uses `requests <http://www.python-requests.org/en/latest/>`_.


-----
Toggl
-----

`Toggl <https://www.toggl.com>`_ is free time tracking software.

--------
Features
--------
- Handles authentication for you: only need to provide your API token once
- The most complete Python wrapper: implements all of v8 API.
- Convenient install from PyPI
- Easy to make requests to custom URLs
- Python2 and Python3 compatible

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

--------------
Custom Request
--------------

Let's pretend that a new endpoint is released, for a new Toggl object: Addresses. This hypothetical endpoint is located at ``https://www.toggl.com/api/v8/addresses``. We can GET all addresses, GET a specific address by ID, or POST to create a new address.

We can use the methods on the Toggl client, so we don't have to wait for a new version of togglwrapper that supports the new endpoint:

.. code-block:: python

    >>> from togglwrapper import Toggl
    >>> toggl = Toggl('your_api_token')
    >>> toggl.get('/addresses')
    ...
    >>> toggl.get('/addresses/{address_id}')
    ...
    >>> toggl.post('/addresses', data={"address": {"name": "Billing Address 1", "address": "123 Main St."}})
    ...


``toggl.put`` and ``toggl.delete`` are also available.


-------------------
Documentation
-------------------
Find the full documentation here: http://togglwrapper.readthedocs.org/en/latest/

---------------------------
API Endpoints Documentation
---------------------------

For full details on what fields are required, and what endpoints are available, see the `Toggl API docs <https://github.com/toggl/toggl_api_docs>`_
