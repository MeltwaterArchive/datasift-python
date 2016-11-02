from __future__ import print_function

from datetime import datetime
from dateutil import parser
import six


class OutputMapper(object):
    def __init__(self, date_strings):

        self.date_strings = date_strings

        self.output_map = {
            "created_at": 'date',
            "dpu": 'float_handler',
            "start": 'date',
            "end": 'date',
            "request_time": 'date',
            "last_success": 'date',
            "updated_at": 'date',
            "reset_at": 'date'
        }

    def float_handler(self, d):
        return float(d)

    def date(self, d):
        if isinstance(d, list):
            return list(map(self.date, d))
        if isinstance(d, six.string_types):
            if d.isdigit():
                d = int(d)
            else:
                if self.date_strings:
                    return str(parser.parse(d))
                return parser.parse(d)
        if isinstance(d, six.integer_types):
            if self.date_strings:
                return str(datetime.fromtimestamp(d))
            return datetime.fromtimestamp(d)
        return d

    def outputmap(self, data):
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
                self.outputmap(item)
        elif isinstance(data, dict):
            for map_target in self.output_map:
                if map_target in data:
                    data[map_target] = getattr(self, self.output_map[map_target])(data[map_target])
            for item in data.values():
                self.outputmap(item)