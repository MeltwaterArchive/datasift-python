import json


class ListReplace(object):
    """ Represents the DataSift Dynamic Lists Replacement API

        http://dev.datasift.com/pickledb
    """
    def __init__(self, request):
        self.request = request.with_prefix('list/replace')

    def start(self, id):
        """ Creates a replacement Dynamic List.

            Uses the API documentated at http://dev.datasift.com/docs/rest-api/listreplacestart

            :param id: id of the list you would like to replace
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("start", data=dict(list_id=id))

    def add(self, id, items):
        """ Adds one or more items to a Replacement Dynamic List.

            Uses the API documentated at http://dev.datasift.com/docs/rest-api/listreplaceadd

            :param id: id of the list to add items to
            :type id: str
            :param items: items to add to the list
            :type name: str, int, List of str or int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("add", data=dict(id=id, items=json.dumps(items)))

    def commit(self, id):
        """ Complete the replacement operation, replacing the original Dynamic List with this Dynamic List.

            Uses the API documentated at http://dev.datasift.com/docs/rest-api/listreplacecommit

            :param id: id of the replacement list to process
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("commit", data=dict(id=id))

    def abort(self, id):
        """ Deletes a replacement Dynamic List.

            Uses the API documentated at http://dev.datasift.com/docs/rest-api/listreplaceabort

            :param id: id of the replacement list to abort
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("abort", data=dict(id=id))


class List(object):
    """ Represents the DataSift Dynamic Lists API.

        http://dev.datasift.com/pickledb
    """
    def __init__(self, request):
        self.request = request.with_prefix('list')
        self.replace = ListReplace(request)

    def create(self, list_type, name):
        """ Creates a new Dynamic List of the given type.

            Uses the API documentated at http://dev.datasift.com/docs/rest-api/listcreate

            :param list_type: type of list to create, can be int or str.
            :type list_type: Class
            :param name: name to give the created list
            :type name: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        if list_type == int:
            t = "integer"
        else:
            t = "text"
        return self.request.post("create", data=dict(type=t, name=name))

    def get(self):
        """ Get the list of all your Dynamic Lists

            Uses the API documented at http://dev.datasift.com/docs/rest-api/listget

            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.get("get")

    def add(self, id, items):
        """ Adds one or more items to a Dynamic List.

            Uses the API documented at http://dev.datasift.com/docs/rest-api/listadd

            :param id: id of the list to add items to
            :type id: str
            :param items: items to add to the list
            :type name: str, int, List of str or int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("add", data=dict(id=id, items=json.dumps(items)))

    def remove(self, id, items):
        """ Removes one or more items from a Dynamic List.

            Uses the API documented at http://dev.datasift.com/docs/rest-api/listremove

            :param id: id of the list to remove items from
            :type id: str
            :param items: items to remove from the list
            :type items: str, int, List of str or int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("remove", data=dict(id=id, items=json.dumps(items)))

    def contains(self, id, items):
        """ Checks if a Dynamic List contains one or more items.

            Uses the API documented at http://dev.datasift.com/docs/rest-api/listexists

            :param id: id of the list to check
            :type id: str
            :param items: items to check existance of in the list
            :type items: str, int, List of str or int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.get("exists", params=dict(id=id, items=json.dumps(items)))

    def delete(self, id):
        """ Deletes a Dynamic List.

            Uses the API documented at http://dev.datasift.com/docs/rest-api/listdelete

            :param id: id of the list to delete
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post("delete", data=dict(id=id))
