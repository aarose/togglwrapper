.. _quickstart:

Quickstart
==========

Example Usage
-------------

.. code-block:: python

    >>> from togglwrapper import Toggl
    >>> toggl = Toggl('your_api_token')
    >>> toggl.User.get()
    {
        u'data': {
            u'achievements_enabled': True,
            u'api_token': u'your_api_token',
            u'email': u'your_email@domain.com',
            u'fullname': u'Your Name',
            ...
        }
    }
    >>> toggl.Workspaces.get()
    [{
        u'admin': True,
        u'api_token': u'your_api_token',
        u'id': 1234,
        ...
    }]
    >>> toggl.Clients.create({"client":{"name":"Very Big Company", "wid": 1234}})
    {
        u'data': {
            u'id': 294021,
            u'name': u'Very Big Company',
            u'wid': 1234,
        }
    }


Creating a Custom Request
-------------------------

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
