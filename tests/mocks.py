from httmock import response, all_requests, urlmatch, HTTMock
import json

@all_requests
def failed_compilation_of_csdl(url, content):
    return response(400, {"error": "We are unable to parse this stream. At line 1 position 17 we were expecting one of: an operator that can act on strings, integers or float types (==, !=, <, >, >=, <=), followed by a text value;\n or the \"substring\" operator, followed by a text value;\n or <predicate.contains_parameters>, followed by a list of comma separated strings;\n or the \"in\" operator for strings, followed by a list of comma separated strings;\n or <predicate.contains_parameters>, followed by a quote (\"), followed by a list of comma separated items in a contains near operator's value, followed by a colon (:), followed by the number of words separation argument in the contains near operator's value, followed by a quote (\");\n or <predicate.contains_parameters>, followed by a text value;\n or the \"in\" operator for dynamic lists, followed by a dynamic list key;\n or <predicate.contains_parameters>, followed by a dynamic list key."}, {'content-type': 'application/json'}, None, 5, content)

@all_requests
def authorization_failed(url, context):
    return response(401, {"error": "Authorization failed)"}, {'content-type': 'application/json'}, None, 5, context)

@all_requests
def internal_server_error(url, context):
    return response(503, "<h1>Internal Server Error</h1>", None, None, 5, context)


@all_requests
def internal_server_error_with_json(url, context):
    return response(503, {"error": "stuff actually blew up a lot"}, None, None, 5, context)


@all_requests
def weird_error(url, context):
    return response(418, {"tea": {"temperature": "hot", "type": "earl grey"}}, None, None, 5, context)

@all_requests
def intentionally_blank(url, context):
    return response(204, {}, None, None, 5, context)

@all_requests
def normal_pull_output():
    data = [{"interaction": {"content": "foo bar"}}, {"interaction": {"content": "other foo bar"}}]
    @all_requests
    def inner_mock(url, context):
        text = "\n".join(map(json.dumps, data))
        return {"status_code": 200, "content": text}
    return (inner_mock, data)

@all_requests
def preview_create(url, context):
    data = {"id": "foo", "created_at": 1364303060}
    return response(202, data)

@all_requests
def source_create(url, context):
    data = json.loads('{"status": "running", "name": "fbp-theguardian", "parameters": {"posts_by_others": true, "likes": true, "comments": true}, "created_at": 1370266044000, "auth": [{"source_id": "d71906e49a3d41e298d76e38782db083", "status": "valid", "expires_at": 1388556000, "identity_id": "51a86d7062464613b7db231d685c4083", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}], "source_type": "facebook_page", "id": "d77906e49a3d41e298d76e38782db083", "resources": [{"source_id": "d7f906e49a3d41e298d76e38782db083", "status": "valid", "parameters": {"url": "http://www.facebook.com/theguardian", "id": 10513336322, "title": "The Guardian"}, "resource_id": "39fbc563e9c14f04b6cb6493ad352b8a"}]}')
    return response(201, data)

@all_requests
def source_update(url, context):
    data = json.loads('{"status": "running", "name": "", "parameters": [], "created_at": 1370266044000, "auth": [{"source_id": "d71906e49a3d41e298d76e38782db083", "status": "valid", "expires_at": 1388556000, "identity_id": "51a86d7062464613b7db231d685c4083", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}, {"source_id": "49fa6dcb175b4a8ca8cbedb8d9015ed0", "status": "valid", "expires_at": 1388556000, "identity_id": "7b1be3a398e646bbb3c7a5cb9717ba45", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}], "source_type": "facebook_page", "id": "d77906e49a3d41e298d76e38782db083", "resources": [{"source_id": "fd2e72e3a7ae40c2a6e86e96381d8165", "status": "valid", "parameters": {"url": "http://www.facebook.com/therollingstones", "id": 8305888286, "title": "The Rolling Stones"}, "resource_id": "d6590d550db94266af6f53884dd65ca4"}, {"source_id": "49fa6dcb175b4a8ca8cbedb8d9015ed0", "status": "valid", "parameters": {"url": "http://www.giffgaff.com", "id": 287613300716, "title": "giffgaffmobile"}, "resource_id": "d43024171340458fb6f124967fd126c1"}]}')
    return response(202, data)

@all_requests
def historics_prepare_live_example(url, context):
    data=json.loads('{"id":"2e0e2376c6dee9b14408","dpus":1.25,"availability":{"start":"1390953600","end":"1390953600","sources":{"twitter":{"augmentations":{"demographic":100,"klout":100,"language":100,"links":100,"meta":100,"salience":100,"trends":100},"versions":["3"],"status":100}}}}')
    return response(202, data)

@all_requests
def rate_limited(url, context):
    return response(403, {"error": "rate limit exceeded"}, {'content-type': 'application/json', 'x-ratelimit-cost': '25', 'x-ratelimit-remaining': '5'}, None, 5, context)

@all_requests
def rate_limit_headers(url, context):
    return response(200, {}, {'x-api-version': '1.1', 'x-ratelimit-remaining': '10000', 'x-served-by': 'ded2587', 'transfer-encoding': 'chunked', 'server': 'nginx/0.8.55', 'connection': 'close', 'x-ratelimit-limit': '10000', 'x-ratelimit-cost': '25', 'date': 'Thu, 06 Feb 2014 13:48:41 GMT', 'p3p': 'CP="CAO PSA"', 'content-type': 'application/json', 'x-cache-control': 'max-age=300, must-revalidate'}, None, 5, context)
