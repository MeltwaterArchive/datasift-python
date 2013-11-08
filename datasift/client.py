from push import *


class Client:
    def __init__(self, **config):
        self.config = config
        self.push = Push(**config)

    def compile(self, csdl):
        """ Compile the given CSDL

        :returns: a dict with a data property of the form
        { "hash": "9fe133a7ee1bd2757f1e26bd78342458","created_at": "2011-05-12 11:18:07","dpu": "0.1"}
        """
        r = req('compile', data={'csdl': csdl}, **self.config)
        return to_response(r)

    def is_valid(self, csdl):
        """ Checks if a given CSDL is valid, returning true if it is or false if it isn't."""
        r = req('validate', data={'csdl': csdl}, **self.config)
        return r.status_code == 200

    def usage(self, period='current'):
        """Check the number of objects processed and delivered for a given time period"""
        r = req('usage', params={'period': period}, method='get', **self.config)
        return to_response(r)

    def dpu(self, stream):
        """Calculate the DPUs for a given stream/hash"""
        r = req('dpu', params={'hash': stream}, method='get', **self.config)
        return to_response(r)

    def balance(self):
        """Determine your credit or DPU balance"""
        r = req('balance', method='get', **self.config)
        return to_response(r)