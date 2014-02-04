from __future__ import print_function

from datetime import datetime
import six


def date_handler_long(d, prefix, endpoint):
    if prefix == "historics" and isinstance(d, six.string_types) and not (" " in d):  # historics sometimes returns string encoded unix timestamps
            d = int(d)
    if d is None:
        return None  # special case for end=None coming out of push
    if isinstance(d, six.string_types):
        return datetime.strptime(d, "%a, %d %b %Y %H:%M:%S +0000")  # rfc2822 email dates
    else:
        return datetime.fromtimestamp(d)  # standard UNIX timestamp


def date_handler_short(d, prefix, endpoint):
    if isinstance(d, six.string_types):
        return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")  # short datetime with no timezone data
    elif isinstance(d, int):
        return datetime.fromtimestamp(d)  # standard UNIX timestamp


def float_handler(d, p, e):
    return float(d)

output_map = {
    "created_at": date_handler_short,
    "dpu": float_handler,
    "start": date_handler_long,
    "end": date_handler_long,
    "request_time": lambda d, p, e: datetime.fromtimestamp(d)
}


def outputmapper(data, prefix, endpoint):
    """ Internal function used to traverse a data structure and map the contents onto python-friendly objects inplace.

        This uses recursion, so try not to pass in anything that's over 255 objects deep.

        :param data: data structure
        :type data: any
        :param prefix: endpoint family, eg. sources, historics
        :type prefix: str
        :param endpoint: endpoint being called on the API
        :type endpoint: str
        :returns: Nothing, edits inplace
    """
    if isinstance(data, list):
        for item in data:
            outputmapper(item, prefix, endpoint)
    elif isinstance(data, dict):
        for map_target in output_map:
            if map_target in data:
                data[map_target] = output_map[map_target](data[map_target], prefix, endpoint)
        for item in data.values():
            outputmapper(item, prefix, endpoint)
