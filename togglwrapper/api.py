# -*- coding: utf-8 -*-

"""
togglwrapper.api
"""
from __future__ import annotations
import json
from typing import Iterable, Literal, overload

import requests
from requests.auth import HTTPBasicAuth

from .decorators import error_checking, return_json
from .mixins import (
    GetMixin,
    CreateMixin,
    PatchMixin,
    UpdateMixin,
    DataDict,
    DeleteMixin,
)


BASE_URL = "https://api.track.toggl.com/api"
API_VERSION = "v9"
API_URL = "{base}/{version}".format(base=BASE_URL, version=API_VERSION)


class TogglObject(object):
    """Base class for Toggl object representations to inherit from."""

    uri: str | None = None
    prepend_workspace_id: bool | None = None

    def __init__(self, toggl: Toggl) -> None:
        self.toggl = toggl
        self.workspace_id = toggl.workspace_id
        if self.uri is None or self.prepend_workspace_id is None:
            # Helper error for subclasses that forget to specify their own URI
            raise NotImplementedError(
                "Must define a URI and whether to prepend the workspace ID."
            )

    @classmethod
    def _compile_uri(
        cls,
        id: int | None = None,
        ids: Iterable[int] | None = None,
        child_uri: str | None = None,
        parent_uri: str | None = None,
    ) -> str:
        """
        Returns the path to append to the base API URL.

        Args:
            id (int, optional): The ID of the object instance. Defaults to
                None.
            ids (iterable of ints, optional): An iterable of IDs of the
                multiple instances to target. Defaults to None.
            child_uri (str, optional): The sub-URI/path to access child objects
                or methods/actions.
        """
        if id and ids:
            raise Exception("Cannot use both an ID and an iterable of IDs.")
        uri = cls.uri
        if id:
            uri += "/{}".format(id)
        if ids:
            uri += "/{}".format(",".join([str(int_id) for int_id in ids]))
        if parent_uri:
            uri = parent_uri + uri
        if child_uri:
            uri = uri + child_uri
        return uri


class Clients(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    """
    The :class:`Clients <Clients>` object.

    Groups all actions relating to Clients together.
    """

    uri: str = "/clients"
    prepend_workspace_id: bool = True

    # DOESN'T EXIST IN v9
    # def get_projects(
    #     self, client_id: int, active: bool | Literal["both"] = True
    # ) -> requests.Response:
    #     """
    #     Gets the projects associated with the Client with the given ID.

    #     Args:
    #         client_id (int): The ID of the client.
    #         active (bool or string, optional): Must be either True, False, or the string 'both'. Defaults to True.
    #     """
    #     cond1 = active is True
    #     cond2 = active is False
    #     cond3 = active == "both"
    #     if not any((cond1, cond2, cond3)):
    #         raise Exception(
    #             "The 'active' param must be either True, False,", "or 'both'."
    #         )
    #     params = {"active": active}
    #     return super(Clients, self).get(client_id, "/projects", params=params)

    @overload
    def get(self, client_id: int) -> requests.Response:
        """Gets the Client with the given ID."""
        ...

    @overload
    def get(
        self,
        status: Literal["active", "archived", "both"] = "active",
        name: str | None = None,
    ) -> requests.Response:
        """Gets all the Clients."""
        ...

    def get(
        self,
        client_id: int | None = None,
        status: Literal["active", "archived", "both"] = "active",
        name: str | None = None,
    ) -> requests.Response:
        """Gets the Client with the given ID."""
        params = {"status": status}
        if name:
            params["name"] = name
        return super(Clients, self).get(client_id, params=params)


class Dashboard(TogglObject, GetMixin):
    uri: str = "/dashboard/all_activity"
    prepend_workspace_id: bool = True

    def get(self) -> requests.Response:
        """Gets the Dashboard for the Workspace."""
        return super(Dashboard, self).get()


class Projects(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri: str = "/projects"
    prepend_workspace_id: bool = True

    @overload
    def get(self, project_id: int) -> requests.Response:
        """Gets the Project with the given ID."""
        ...

    @overload
    def get(self, params: DataDict) -> requests.Response:
        """Gets all the Projects."""
        ...

    def get(
        self, project_id: int | None = None, params: DataDict | None = None
    ) -> requests.Response:
        return super(Projects, self).get(id=project_id, params=params)

    # Use ProjectUsers instead
    # def get_project_users(self, project_id: int) -> requests.Response:
    #     """Gets the ProjectUsers for the Project with the given ID."""
    #     return super(Projects, self).get(project_id, "/project_users")

    def get_tasks(self, project_id: int) -> requests.Response:
        """Gets the Tasks for the Project with the given ID."""
        return super(Projects, self).get(project_id, "/tasks")

    def get_task(self, project_id: int, task_id: int) -> requests.Response:
        """Gets the Tasks for the Project with the given ID."""
        return super(Projects, self).get(project_id, "/tasks/{}".format(task_id))


class ProjectUsers(
    TogglObject, GetMixin, CreateMixin, PatchMixin, UpdateMixin, DeleteMixin
):
    uri: str = "/project_users"
    prepend_workspace_id: bool = True

    def get(
        self,
        project_ids: list[int] | None = None,
        with_group_members: bool | None = None,
    ) -> requests.Response:
        """Gets the ProjectUsers with the given criteria."""
        params = {}
        if project_ids is not None:
            params["project_ids"] = "".join(
                [str(project_id) for project_id in project_ids]
            )
        if with_group_members is not None:
            params["with_group_members"] = with_group_members
        return super(ProjectUsers, self).get(params=params)


class Tags(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri: str = "/tags"
    prepend_workspace_id: bool = True


class Tasks(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri: str = "/tasks"
    prepend_workspace_id: bool = True

    @overload
    def get(
        self,
        task_id: int,
        project_id: int,
    ) -> requests.Response:
        """Gets the Task with the given IDs."""
        ...

    @overload
    def get(self) -> requests.Response:
        """Gets all the Tasks."""
        ...

    def get(
        self, task_id: int | None = None, project_id: int | None = None
    ) -> requests.Response:
        if project_id is not None:
            return self.toggl.Projects.get_task(project_id, task_id)
        return super(Tasks, self).get(id=task_id)

    def get_for_project(self, project_id: int) -> requests.Response:
        """Gets the Tasks for the Project with the given ID."""
        return self.toggl.Projects.get_tasks(project_id)


class TimeEntries(TogglObject, GetMixin, CreateMixin, PatchMixin, DeleteMixin):
    uri: str = "/time_entries"
    prepend_workspace_id: bool = True

    @overload
    def get(self, id: int) -> requests.Response:
        """Gets the TimeEntry with the given ID."""
        ...

    @overload
    def get(self, start_date: str, end_date: str) -> requests.Response:
        """Gets up to 1000 TimeEntries in the given time range. Dates must be ISO 8601
        date and time strings, e.g. '2013-03-10T15:42:46+02:00'."""
        ...

    @overload
    def get(self) -> requests.Response:
        """Gets up to 1000 TimeEntries from the last 9 days."""
        ...

    def get(
        self,
        id: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> requests.Response:
        """
        Gets a time entry, or time entires in a time range, or the latest ones.

        If neither an ID or time range is given, returns the time entries
        started during the last 9 days. The limit of returned time entries
        is 1000. So only the first 1000 found time entries are returned.

        Args:
            id (int, optional): The ID of the specific instance to get.
                Defaults to None.
            start_date (str, optional): Must be ISO 8601 date and time strings.
                e.g. '2013-03-10T15:42:46+02:00'. Defaults to None.
            end_date (str, optional): Must be ISO 8601 date and time strings.
                e.g. '2013-03-10T15:42:46+02:00'. Defaults to None.
        """
        params = {"start_date": start_date, "end_date": end_date}
        return super(TimeEntries, self).get(id=id, params=params, parent_uri="/me")

    def start(self, data: DataDict) -> requests.Response:
        """Starts a new time entry."""
        return super(TimeEntries, self).create(data=data)

    def stop(self, time_entry_id: int) -> requests.Response:
        """Stops the time entry with the given ID."""
        return super(TimeEntries, self).patch(id=time_entry_id, child_uri="/stop")

    def get_current(self) -> requests.Response:
        """Gets the current running time entry."""
        return super(TimeEntries, self).get(child_uri="/current", parent_uri="/me")


class User(TogglObject, GetMixin, UpdateMixin):
    uri: str = "/me"
    prepend_workspace_id: bool = False

    def get(
        self, related_data: bool = False, since: str | int | None = None
    ) -> requests.Response:
        """
        Gets the User associated with the current API token.

        Args:
            related_data (bool): If True, gets all the workspaces, clients,
                projects, tasks, time entries and tags which the user can see.
                Defaults to False.
            since (str or int, optional): Get objects which have changed after
                a certain time. The value should be a unix timestamp
                (e.g. 1362579886). Defaults to None.
        """
        params = {"since": since}
        if related_data:
            params["with_related_data"] = related_data
        return super(User, self).get(params=params)

    def update(self, data: DataDict) -> requests.Response:
        """
        Updates the user associated with the api token.

        Args:
            data (dict): The dict of information to update for the user.
        """
        return super(User, self).update(data=data)


class Workspaces(TogglObject, GetMixin, UpdateMixin):
    uri: str = "/workspaces"
    prepend_workspace_id: bool = False

    def get_users(self) -> requests.Response:
        """Gets the Users for the Workspace."""
        return super(Workspaces, self).get(self.workspace_id, "/users")

    def get_clients(self) -> requests.Response:
        """Gets the Clients for the Workspace."""
        return super(Workspaces, self).get(self.workspace_id, "/clients")

    def get_projects(self) -> requests.Response:
        """Gets the Projects for the Workspace."""
        return super(Workspaces, self).get(self.workspace_id, "/projects")

    def get_tasks(self) -> requests.Response:
        """Gets the Tasks for the Workspace."""
        return super(Workspaces, self).get(self.workspace_id, "/tasks")

    def get_tags(self) -> requests.Response:
        """Gets the Tags for the Workspace."""
        return super(Workspaces, self).get(self.workspace_id, "/tags")


class Toggl(object):
    """
    Class to collect all Toggl objects in one place.

    Ensures easy authentication, since API credentials only need to be provided
    upon instantiation.
    """

    def __init__(
        self,
        api_token: str,
        organization_id: int,
        workspace_id: int,
        base_url: str = BASE_URL,
        version: str = API_VERSION,
    ) -> None:
        """
        Initializes the Toggl client object.

        Args:
            api_token (str): The Toggl API token. Can be found at
                https://www.toggl.com/app/profile
            workspace_id (int): The ID of the workspace to use.
            base_url (str): The base API URL. Defaults to
                `https://www.toggl.com/api`.
            version (str): The version of the API. Used to compile the full
                URL. Defaults to `v8`.
        """
        self.api_url: str = "{base}/{version}".format(base=base_url, version=version)
        self.organization_id: int = organization_id
        self.workspace_id: int = workspace_id
        self.auth: HTTPBasicAuth = HTTPBasicAuth(api_token, "api_token")
        self.Clients: Clients = Clients(self)
        self.Dashboard: Dashboard = Dashboard(self)
        self.Projects: Projects = Projects(self)
        self.ProjectUsers: ProjectUsers = ProjectUsers(self)
        self.Tags: Tags = Tags(self)
        self.Tasks: Tasks = Tasks(self)
        self.TimeEntries: TimeEntries = TimeEntries(self)
        self.User: User = User(self)
        self.Workspaces: Workspaces = Workspaces(self)

    def signup(self, data: DataDict) -> requests.Response:
        """
        Creates a new user.

        Args:
          data (dict): Contains required and optional fields and values.
        """
        return self.post("/signup", data)

    def invite(self, data: DataDict) -> requests.Response:
        """
        Adds users to the workspace. Sends an email invite to the users.

        Args:
            data (dict): The information needed to invite the right user.
        """
        uri = "/organizations/{organization_id}/invite".format(
            organization_id=self.toggl.organization_id
        )
        return self.toggl.post(uri, data)

    def reset_token(self) -> requests.Response:
        """Deletes the current API Token and returns a new token."""
        return self.post("/me/reset_token")

    @return_json
    @error_checking
    def get(self, uri: str, params: DataDict | None = None) -> requests.Response:
        """
        GETs to the given URI.

        Args:
            uri (str): The URI/path to append to the full API URL.
            params (dict, optional): Extra parameters/querystrings to accompany the GET request.
        """
        full_uri = "{base}{uri}".format(base=self.api_url, uri=uri)
        return requests.get(full_uri, params=params, auth=self.auth)

    @return_json
    @error_checking
    def post(self, uri: str, data: DataDict | None = None) -> requests.Response:
        """
        POSTs to the given URI.

        Args:
            uri (str): The URI/path to append to the full API URL.
            data (optional): dict, bytes, or file-like object to POST.
        """
        full_uri = "{base}{uri}".format(base=self.api_url, uri=uri)
        payload = json.dumps(data) if data is not None else None
        return requests.post(full_uri, data=payload, auth=self.auth)

    @return_json
    @error_checking
    def put(self, uri: str, data: DataDict) -> requests.Response:
        """
        PUTs to the given URI with a data.

        Args:
            uri (str): The URI/path to append to the full API URL.
            data: dict, bytes, or file-like object to PUT.
        """
        full_uri = "{base}{uri}".format(base=self.api_url, uri=uri)
        payload = json.dumps(data)
        return requests.put(full_uri, data=payload, auth=self.auth)

    @return_json
    @error_checking
    def patch(self, uri: str, data: DataDict) -> requests.Response:
        """
        PATCHes to the given URI with a data.

        Args:
            uri (str): The URI/path to append to the full API URL.
            data: dict, bytes, or file-like object to PATCH.
        """
        full_uri = "{base}{uri}".format(base=self.api_url, uri=uri)
        payload = json.dumps(data)
        return requests.patch(full_uri, data=payload, auth=self.auth)

    @error_checking
    def delete(self, uri: str) -> requests.Response:
        """DELETEs to the given URI."""
        full_uri = "{base}{uri}".format(base=self.api_url, uri=uri)
        return requests.delete(full_uri, auth=self.auth)
