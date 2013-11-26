

class Config(object):
    def __init__(self, user, apikey, proxies=None, timeout=None, verify=None):
        self.user = user
        self.apikey = apikey
        self.proxies = proxies
        self.timeout = timeout
        self.verify = verify

