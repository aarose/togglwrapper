.. _api:

.. module:: togglwrapper

Toggl
-----

.. autoclass:: togglwrapper.Toggl
    :inherited-members:


Toggl Classes
-------------

.. module:: togglwrapper.api

These can all be accessed from an instantiated Toggl client. For example:

.. code-block:: python

    >>> toggl = Toggl('api_token')
    >>> toggl.Clients.get()
    ...
    >>> toggl.Dashboard.get(3542)
    ...
    >>> toggl.Workspaces.get()
    ...


.. autoclass:: togglwrapper.api.Clients
    :inherited-members:

.. autoclass:: togglwrapper.api.Dashboard
    :inherited-members:

.. autoclass:: togglwrapper.api.Projects
    :inherited-members:

.. autoclass:: togglwrapper.api.ProjectUsers
    :inherited-members:

.. autoclass:: togglwrapper.api.Tags
    :inherited-members:

.. autoclass:: togglwrapper.api.Tasks
    :inherited-members:

.. autoclass:: togglwrapper.api.TimeEntries
    :inherited-members:

.. autoclass:: togglwrapper.api.User
    :inherited-members:

.. autoclass:: togglwrapper.api.Workspaces
    :inherited-members:

.. autoclass:: togglwrapper.api.WorkspaceUsers
    :inherited-members:


Exceptions
----------

.. module:: togglwrapper.exceptions

.. autoexception:: togglwrapper.exceptions.AuthError
