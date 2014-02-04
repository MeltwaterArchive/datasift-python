class Config(object):
    """Configuration object for the DataSift client

        :param user: username for the DataSift platform
        :type user: str
        :param apikey: API key for the DataSift platform
        :type apikey: str
        :param proxies: (optional) dict of proxies for requests to use, of the form {"https": "http://me:password@myproxyserver:port/" }
        :type proxies: dict
        :param timeout: (optional) seconds to wait for HTTP connections
        :type timeout: float
        :param verify: (optional) whether to verify SSL certificates
        :type verify: bool
    """
    def __init__(self, user, apikey, proxies=None, timeout=None, verify=None):
        self.user = user
        self.key = apikey
        self.proxies = proxies
        self.timeout = timeout
        self.verify = verify
