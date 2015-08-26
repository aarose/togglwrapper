# Toggl Wrapper

Python library to easily interface with Toggl's API. Only supports the main Toggl API, not the Reports API (coming soon).


## Toggl

Toggl (www.toggl.com) is free time tracking software.


## Quick setup
    pip install togglwrapper
    
    
    $ python
    >>> from togglwrapper import Toggl
    >>> toggl = Toggl('api_key_goes_here')
    >>> toggl.User.get()


## Methods and Classes
* toggl.Clients
* toggl.Dashboard
* toggl.Projects
* toggl.ProjectUsers
* toggl.Tags
* toggl.Tasks \*user associated with the api token must be a Pro member
* toggl.TimeEntries
* toggl.User
* toggl.Workspaces
* toggl.WorkspaceUsers
* toggl.signup()
* toggl.reset\_token()


## API reference

For full details on what fields are required, and what endpoints are available, see the Toggl API docs: https://github.com/toggl/toggl_api_docs
