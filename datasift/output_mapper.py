from datetime import datetime
import six

class OutputMapper():
    def date_handler_long(d, prefix, endpoint):
            if d==None:
                return None  # special case for end=None coming out of push
            if isinstance(d, six.string_types):
                return datetime.strptime(d, "%a, %d %b %Y %H:%M:%S +0000")
            else:
                return datetime.fromtimestamp(d)

    def date_handler_short(d, prefix, endpoint):
            if prefix=="source" and endpoint in ["create", "update"]:
                return datetime.fromtimestamp(d/1000)
            if isinstance(d, six.string_types):
                return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
            else:
                return datetime.fromtimestamp(d)

    def float_handler(d, p, e):
        return float(d)
    output_map = {
            "created_at": date_handler_short,
            "dpu": float_handler,
            "start": date_handler_long,
            "end": date_handler_long
            }

    def __call__(self, input_dict, prefix, endpoint):
        for map_target in self.output_map:
            if map_target in input_dict:
                input_dict[map_target] = self.output_map[map_target](input_dict[map_target], prefix, endpoint)
