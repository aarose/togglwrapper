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
    u'at': u'2015-08-26T20:08:43+00:00',
    u'beginning_of_week': 1,
    u'created_at': u'2015-06-10T19:06:43+00:00',
    u'date_format': u'MM/DD/YYYY',
    u'default_wid': 979325,
    u'duration_format': u'improved',
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
    u'at': u'2015-06-10T19:06:43+00:00',
    u'campaign': False,
    u'default_currency': u'USD',
    u'default_hourly_rate': 0,
    u'ical_enabled': True,
    u'id': 1234,
    u'name': u"Your workspace",
    u'only_admins_may_create_projects': False,
    u'only_admins_see_billable_rates': False,
    u'only_admins_see_team_dashboard': False,
    u'premium': False,
    u'profile': 0,
    u'projects_billable_by_default': True,
    u'rounding': 1,
    u'rounding_minutes': 0,
    u'subscription': {u'description': u'Free'}}]
    >>> toggl.Clients.create({"client":{"name":"Very Big Company", "wid": 1234}})
    {u'data': {u'id': 294021, u'name': u'Very Big Company', u'wid': 1234}}
    ...


-------------------
Methods and Classes
-------------------
- toggl.Clients
- toggl.Dashboard
- toggl.Projects
- toggl.ProjectUsers
- toggl.Tags
- toggl.Tasks `NOTE: user associated with the api token must be a Pro member`
- toggl.TimeEntries
- toggl.User
- toggl.Workspaces
- toggl.WorkspaceUsers
- toggl.signup()
- toggl.reset_token()


---------------------------
API Endpoints Documentation
---------------------------

For full details on what fields are required, and what endpoints are available, see the `Toggl API docs <https://github.com/toggl/toggl_api_docs>`_
