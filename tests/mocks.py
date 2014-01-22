from httmock import response, all_requests, urlmatch, HTTMock

@all_requests
def failed_compilation_of_csdl(url, content):
    return response(400, {"error": "We are unable to parse this stream. At line 1 position 17 we were expecting one of: an operator that can act on strings, integers or float types (==, !=, <, >, >=, <=), followed by a text value;\n or the \"substring\" operator, followed by a text value;\n or <predicate.contains_parameters>, followed by a list of comma separated strings;\n or the \"in\" operator for strings, followed by a list of comma separated strings;\n or <predicate.contains_parameters>, followed by a quote (\"), followed by a list of comma separated items in a contains near operator's value, followed by a colon (:), followed by the number of words separation argument in the contains near operator's value, followed by a quote (\");\n or <predicate.contains_parameters>, followed by a text value;\n or the \"in\" operator for dynamic lists, followed by a dynamic list key;\n or <predicate.contains_parameters>, followed by a dynamic list key."}, {'content-type': 'application/json'}, None, 5, content)

@all_requests
def authorization_failed(url, context):
    return response(403, {"error": "Authorization failed)"}, {'content-type': 'application/json'}, None, 5, context)
