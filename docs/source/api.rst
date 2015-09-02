.. _api:

.. module:: togglwrapper

Toggl
-----

.. autoclass:: togglwrapper.Toggl
    :inherited-members:


Child Classes
-------------

These can all be accessed from an instantiated Toggl client. For example:

.. code-block::python

    >>> toggl = Toggl('api_token')
    >>> toggl.Clients.get()


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

.. autoexception:: togglwrapper.exceptions.AuthError
