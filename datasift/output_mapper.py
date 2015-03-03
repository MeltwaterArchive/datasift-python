from __future__ import print_function

from datetime import datetime
from dateutil import parser
import six


def float_handler(d):
    return float(d)


def date(d):
    if isinstance(d, list):
        return list(map(date, d))
    if isinstance(d, six.string_types):
        if d.isdigit():
            d = int(d)
        else:
            return parser.parse(d)
    if isinstance(d, six.integer_types):
        return datetime.fromtimestamp(d)
    return d

output_map = {
    "created_at": date,
    "dpu": float_handler,
    "start": date,
    "end": date,
    "request_time": date,
    "last_success": date
}


def outputmapper(data):
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
            outputmapper(item)
    elif isinstance(data, dict):
        for map_target in output_map:
            if map_target in data:
                data[map_target] = output_map[map_target](data[map_target])
        for item in data.values():
            outputmapper(item)
