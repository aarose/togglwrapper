class GetMixin(object):
    """ Mixin to add get methods to a class. """
    def get(self, id=None, child_uri=None, params=None):
        """
        Get the array of objects, or a specific instance by ID.

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


class CreateMixin(object):
    """ Mixin to add create methods to a class. """
    def create(self, data):
        """
        Create a new instance of the object type.

        Args:
            data (dict): The dict of data to POST.
        """
        return self.toggl.post(self.uri, data)


class UpdateMixin(object):
    """ Mixin to add update methods to a class. """
    def update(self, id=None, ids=None, child_uri=None, data=None):
        """ Update a specific instance by ID, or update multiple instances. """
        uri = self._compile_uri(id=id, ids=ids, child_uri=child_uri)
        return self.toggl.put(uri, data)


class DeleteMixin(object):
    """ Mixin to add delete methods to a class. """
    def delete(self, id=None, ids=None):
        """ Delete a specific instance by ID, or delete multiple instances. """
        if not any((id, ids)):
            raise Exception('Must provide either an ID or an iterable of IDs.')
        return self.toggl.delete(self._compile_uri(id=id, ids=ids))
