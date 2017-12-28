# -*- coding: utf-8 -*-

"""
togglwrapper.mixins
-------------------

This module contains mixins for TogglObject subclasses. The common CRUD
(create, read, update, delete) methods are all used by different Toggl objects,
but in different combinations. Some objects have endpoints for all four
methods, but some only implement two or three of the four (e,g, User only
allows updating and getting, not deleting or creating). Separating the
methods out into mixins allows easy mix-and-matching, and re-useability.
"""


class GetMixin(object):
    """ Mixin to add get methods to a class. """
    def get(self, id=None, child_uri=None, params=None):
        """
        Gets the array of objects, or a specific instance by ID.

        Args:
            id (int, optional): The ID of a specific instance of the Object.
                If none provided, the array of all available instances is
                retrieved, provided that an endpoint exists for it.  Defaults
                to None.
            child_uri (str, optional): The URI of the child Object or subpath.
                e.g. If we wanted the Clients of a Workspace, where the
                Workspace is the parent object, the child URI is '/clients'.
                Defaults to None.
            params (dict, optional): The dictionary of additional params to
                include in as the querystring, appended to the URL. Keys with
                values of None will be ignored. Defaults to None.
        """
        uri = self._compile_uri(id, child_uri=child_uri)
        return self.toggl.get(uri, params=params)

    def _valid_lower_values(self, value, name, allowed):
        """
        Validates and package the params in dict used as requests get query parameter.

        Args:
            name (str): Name of the param
            value (str|bool): Value of the param.
            allowed ([str]): Case insensitive allowed values

        """
        try:
            value_ = str(value).lower()
            if value_ in allowed:
                return {name: value_}
            raise ValueError('Param %s do not accept %s only %s.' %
                             (name, value, allowed))
        except AttributeError:  # Invalid param value
            raise ValueError('Invalid param %s.' % name)

    def param_bool(self, name, value):
        """ Returns the bool values used as params through the toggl API.

        Args:
            name (str): Name of the param
            value (str|bool): Value of the param.
        """
        allowed = ['true', 'false']
        return self._valid_lower_values(value, name, allowed) if value is not None else {}

    def param_bool_both(self, name, value):
        """ Returns the bool or both values used as params through the toggl API.

        Args:
            name (str): Name of the param
            value (str|bool): Value of the param.
        """
        allowed = ['true', 'false', 'both']
        return self._valid_lower_values(value, name, allowed) if value is not None else {}


class CreateMixin(object):
    """ Mixin to add create methods to a class. """
    def create(self, data):
        """
        Creates a new instance of the object type.

        Args:
            data (dict): The dict of information needed to create a new object.
        """
        return self.toggl.post(self.uri, data)


class UpdateMixin(object):
    """ Mixin to add update methods to a class. """
    def update(self, id=None, ids=None, child_uri=None, data=None):
        """
        Updates a specific instance by ID, or update multiple instances.

        Args:
            id (int, optional): The ID of the instance to update. Defaults to
                None.
            ids (iterable of ints, optional): An iterable of IDs of instances
                to update. Not all objects allow multiple instances to be
                updated at once - see Toggl's API Documentation to see where
                this is allowed. Defaults to None.
            child_uri (str, optional): The URI/path to append to the object's
                URI, to update. Defaults to None.
            data (dict, optional): The dict of information to update the
                object(s). Defaults to None.
        """
        uri = self._compile_uri(id=id, ids=ids, child_uri=child_uri)
        return self.toggl.put(uri, data)


class DeleteMixin(object):
    """ Mixin to add delete methods to a class. """
    def delete(self, id=None, ids=None):
        """
        Deletes a specific instance by ID, or delete multiple instances.

        Args:
            id (int, optional): The ID of the instance to delete. Defaulta to
                None.
            ids (iterable of ints, optional): An iterable of IDs of instances
                to delete. Not all objects allow for deleting multiple
                instances at once. See Toggl's API Documentation to see where
                this is allowed. Defaults to None.
        """
        if not any((id, ids)):
            raise Exception('Must provide either an ID or an iterable of IDs.')
        return self.toggl.delete(self._compile_uri(id=id, ids=ids))
