from __future__ import print_function

from datetime import datetime
import six


def date_handler_long(d, prefix, endpoint):
    if prefix == "historics" and isinstance(d, six.string_types) and not (" " in d):
            d = int(d)
    if d is None:
        return None  # special case for end=None coming out of push
    if isinstance(d, six.string_types):
        return datetime.strptime(d, "%a, %d %b %Y %H:%M:%S +0000")
    else:
        return datetime.fromtimestamp(d)


def date_handler_short(d, prefix, endpoint):
    if isinstance(d, six.string_types):
        return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    elif isinstance(d, int):
        return datetime.fromtimestamp(d)


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
    if isinstance(data, list):
        for item in data:
            outputmapper(item, prefix, endpoint)
    if isinstance(data, dict):
        for map_target in output_map:
            if map_target in data:
                data[map_target] = output_map[map_target](data[map_target], prefix, endpoint)
        for item in data.values():
            if isinstance(data, (dict, list)):
                outputmapper(item, prefix, endpoint)
