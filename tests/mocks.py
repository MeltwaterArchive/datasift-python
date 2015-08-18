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
    data = json.loads('{"status": "running", "name": "fbp-theguardian", "parameters": {"posts_by_others": true, "likes": true, "comments": true}, "created_at": 1370266044, "auth": [{"source_id": "d71906e49a3d41e298d76e38782db083", "status": "valid", "expires_at": 1388556000, "identity_id": "51a86d7062464613b7db231d685c4083", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}], "source_type": "facebook_page", "id": "d77906e49a3d41e298d76e38782db083", "resources": [{"source_id": "d7f906e49a3d41e298d76e38782db083", "status": "valid", "parameters": {"url": "http://www.facebook.com/theguardian", "id": 10513336322, "title": "The Guardian"}, "resource_id": "39fbc563e9c14f04b6cb6493ad352b8a"}]}')
    return response(201, data)

@all_requests
def source_update(url, context):
    data = json.loads('{"status": "running", "name": "", "parameters": [], "created_at": 1370266044, "auth": [{"source_id": "d71906e49a3d41e298d76e38782db083", "status": "valid", "expires_at": 1388556000, "identity_id": "51a86d7062464613b7db231d685c4083", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}, {"source_id": "49fa6dcb175b4a8ca8cbedb8d9015ed0", "status": "valid", "expires_at": 1388556000, "identity_id": "7b1be3a398e646bbb3c7a5cb9717ba45", "parameters": {"value": "363056350669209|09af1ce9c5d8d23147ec4eeb9a33aac2"}}], "source_type": "facebook_page", "id": "d77906e49a3d41e298d76e38782db083", "resources": [{"source_id": "fd2e72e3a7ae40c2a6e86e96381d8165", "status": "valid", "parameters": {"url": "http://www.facebook.com/therollingstones", "id": 8305888286, "title": "The Rolling Stones"}, "resource_id": "d6590d550db94266af6f53884dd65ca4"}, {"source_id": "49fa6dcb175b4a8ca8cbedb8d9015ed0", "status": "valid", "parameters": {"url": "http://www.giffgaff.com", "id": 287613300716, "title": "giffgaffmobile"}, "resource_id": "d43024171340458fb6f124967fd126c1"}]}')
    return response(202, data)

@all_requests
def historics_prepare_live_example(url, context):
    data=json.loads('{"id":"2e0e2376c6dee9b14408","dpus":1.25,"availability":{"start":"1390953600","end":"1390953600","sources":{"tumblr":{"augmentations":{"demographic":100,"klout":100,"language":100,"links":100,"meta":100,"salience":100,"trends":100},"versions":["3"],"status":100}}}}')
    return response(202, data)

@all_requests
def rate_limited(url, context):
    return response(403, {"error": "rate limit exceeded"}, {'content-type': 'application/json', 'x-ratelimit-cost': '25', 'x-ratelimit-remaining': '5'}, None, 5, context)

@all_requests
def rate_limit_headers(url, context):
    return response(200, {}, {'x-api-version': '1.1', 'x-ratelimit-remaining': '10000', 'x-served-by': 'ded2587', 'transfer-encoding': 'chunked', 'server': 'nginx/0.8.55', 'connection': 'close', 'x-ratelimit-limit': '10000', 'x-ratelimit-cost': '25', 'date': 'Thu, 06 Feb 2014 13:48:41 GMT', 'p3p': 'CP="CAO PSA"', 'content-type': 'application/json', 'x-cache-control': 'max-age=300, must-revalidate'}, None, 5, context)

@all_requests
def pull_json_meta(url, context):
    return response(200, {u'count': 2, u'delivered_at': u'Fri, 17 Aug 2012 14:23:00 +0000', u'interactions': [{u'tumblr': {u'links': [u'http://4sq.com/NLM3gD'], u'text': u'I like ice cream', u'created_at': u'Fri, 17 Aug 2012 14:13:08 +0000', u'source': u'<a href="http://example.com" rel="nofollow">example</a>', u'place': {u'full_name': u'Cafe On the Common, Waltham', u'url': u'http://johndoe.tumblr.com/', u'country': u'United States', u'place_type': u'poi', u'country_code': u'US', u'id': u'90ad0a08b3333d6d', u'name': u'Cafe On the Common'}, u'user': {u'lang': u'en', u'utc_offset': -18000, u'id_str': u'11111111', u'statuses_count': 9689, u'name': u'John Doe', u'friends_count': 2016, u'url': u'http://about.me/John Doe', u'created_at': u'Fri, 30 Nov 2007 21:26:38 +0000', u'time_zone': u'Eastern Time (US & Canada)', u'followers_count': 2054, u'screen_name': u'johndoe', u'location': u'London', u'geo_enabled': True, u'listed_count': 118, u'id': 11111111, u'description': u'all my tweets...'}, u'domains': [u'4sq.com'], u'mentions': [u'beyonce', u'ladygaga'], u'geo': {u'latitude': 42.376104, u'longitude': -71.237189}, u'id': u'111111111111111111'}, u'interaction': {u'author': {u'username': u'johndoe', u'link': u'http://johndoe.tumblr.com/', u'name': u'John Doe', u'avatar': u'http://a0.twimg.com/profile_images/1111111111/example.jpeg', u'id': 10750902}, u'geo': {u'latitude': 42.376104, u'longitude': -71.237189}, u'created_at': u'Fri, 17 Aug 2012 14:13:08 +0000', u'content': u'I like ice cream!', u'source': u'web', u'link': u'http://johndoe.tumblr.com/', u'type': u'tumblr', u'id': u'1e1e875ab43fa233e074337458bc1dca'}}, {u'tumblr': {u'links': [u'http://4sq.com/NMH47L'], u'text': u'I love ice cream', u'created_at': u'Fri, 17 Aug 2012 14:13:09 +0000', u'source': u'<a href="http://example.com" rel="nofollow">example</a>', u'place': {u'full_name': u'Willow Farm', u'url': u'http://johndoe.tumblr.com/', u'country': u'United States', u'place_type': u'poi', u'country_code': u'US', u'id': u'e5ac52573b5f3333', u'name': u'Willow Farm'}, u'user': {u'lang': u'en', u'utc_offset': -18000, u'id_str': u'11111111', u'statuses_count': 10073, u'name': u'John Doe', u'friends_count': 533, u'created_at': u'Sun, 26 Apr 2009 23:38:45 +0000', u'time_zone': u'Quito', u'followers_count': 444, u'screen_name': u'John Doe', u'location': u'Main street', u'geo_enabled': True, u'listed_count': 9, u'id': 11111111, u'description': u'Man of mystery\n'}, u'domains': [u'4sq.com'], u'geo': {u'latitude': 41.48454863, u'longitude': -72.79693173}, u'id': u'111111111111111111'}, u'interaction': {u'author': {u'username': u'JohnDoe', u'link': u'http://johndoe.tumblr.com/', u'name': u'John Doe', u'avatar': u'http://static.tumblr.com/111111.jpg', u'id': 11111111}, u'geo': {u'latitude': 41.48454863, u'longitude': -72.79693173}, u'created_at': u'Fri, 17 Aug 2012 14:13:09 +0000', u'content': u'I love ice cream!', u'source': u'example', u'link': u'http://johndoe.tumblr.com/post/111111111111111111', u'type': u'tumblr', u'id': u'1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a'}, u'demographic': {u'gender': u'mostly_male'}}], u'hash_type': u'stream', u'hash': u'c426dd575d435e5bc68a6edf125026c4', u'id': u'93186020677f1881aab7cddb28fa805c'}, {"X-DataSift-Format": "json_meta"})

@all_requests
def pull_json_array(url, context):
    return response(200, '[{"tumblr": {"links": ["http://4sq.com/NLM3gD"], "text": "I like ice cream", "created_at": "Fri, 17 Aug 2012 14:13:08 +0000", "source": "<a href=\\"http://example.com\\" rel=\\"nofollow\\">example</a>", "place": {"full_name": "Cafe On the Common, Waltham", "url": "http://johndoe.tumblr.com/", "country": "United States", "place_type": "poi", "country_code": "US", "id": "90ad0a08b3333d6d", "name": "Cafe On the Common"}, "user": {"lang": "en", "utc_offset": -18000, "id_str": "11111111", "statuses_count": 9689, "name": "John Doe", "friends_count": 2016, "url": "http://about.me/John Doe", "created_at": "Fri, 30 Nov 2007 21:26:38 +0000", "time_zone": "Eastern Time (US & Canada)", "followers_count": 2054, "screen_name": "johndoe", "location": "London", "geo_enabled": true, "listed_count": 118, "id": 11111111, "description": "all my tweets..."}, "domains": ["4sq.com"], "mentions": ["beyonce", "ladygaga"], "geo": {"latitude": 42.376104, "longitude": -71.237189}, "id": "111111111111111111"}, "interaction": {"author": {"username": "johndoe", "link": "http://johndoe.tumblr.com/", "name": "John Doe", "avatar": "http://a0.twimg.com/profile_images/1111111111/example.jpeg", "id": 10750902}, "geo": {"latitude": 42.376104, "longitude": -71.237189}, "created_at": "Fri, 17 Aug 2012 14:13:08 +0000", "content": "I like ice cream!", "source": "web", "link": "http://johndoe.tumblr.com/posts/1111111", "type": "tumblr", "id": "1e1e875ab43fa233e074337458bc1dca"}}, {"tumblr": {"links": ["http://4sq.com/NMH47L"], "text": "I love ice cream", "created_at": "Fri, 17 Aug 2012 14:13:09 +0000", "source": "<a href=\\"http://example.com\\" rel=\\"nofollow\\">example</a>", "place": {"full_name": "Willow Farm", "url": "http://johndoe.tumblr.com/", "country": "United States", "place_type": "poi", "country_code": "US", "id": "e5ac52573b5f3333", "name": "Willow Farm"}, "user": {"lang": "en", "utc_offset": -18000, "id_str": "11111111", "statuses_count": 10073, "name": "John Doe", "friends_count": 533, "created_at": "Sun, 26 Apr 2009 23:38:45 +0000", "time_zone": "Quito", "followers_count": 444, "screen_name": "John Doe", "location": "Main street", "geo_enabled": true, "listed_count": 9, "id": 11111111, "description": "Man of mystery\\n"}, "domains": ["4sq.com"], "geo": {"latitude": 41.48454863, "longitude": -72.79693173}, "id": "111111111111111111"}, "interaction": {"author": {"username": "JohnDoe", "link": "http://johndoe.tumblr.com/", "name": "John Doe", "avatar": "http://a0.twimg.com/profile_images/1111111111/example.jpg", "id": 11111111}, "geo": {"latitude": 41.48454863, "longitude": -72.79693173}, "created_at": "Fri, 17 Aug 2012 14:13:09 +0000", "content": "I love ice cream!", "source": "web", "link": "http://johndoe.tumblr.com/", "type": "tumblr", "id": "1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a"}, "demographic": {"gender": "mostly_male"}}]', {"X-DataSift-Format": "json_array"})
