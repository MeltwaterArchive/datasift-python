import pandas as pd
import datetime
from datasift import Client


def to_timestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

class Recording:

    def __init__(self,client,hash):
        self.client = client
        self.hash = hash
        self.filter = None
        self.start = None
        self.end = None

    def get(self):
        return RecordingInfo(self.client.pylon.get(self.hash))

    def set_period(self, start=None, end=None):
        if not start is None:
            self.start = to_timestamp(start)
        if not end is None:
            self.end = to_timestamp(end)

    def set_filter(self, csdl):
        self.filter = csdl

    def freq_dist(self,target,threshold):
        parameters = {'analysis_type': 'freqDist', 'parameters': {'threshold': threshold, 'target': target }}
        return FreqDistResult(self.client.pylon.analyze(self.hash, parameters, filter=self.filter,start=self.start,end=self.end))

    def time_series(self,interval='hour',span=1):
        parameters = {'analysis_type': 'timeSeries', 'parameters': {'interval': interval, 'span': span }}
        return TimeSeriesResult(self.client.pylon.analyze(self.hash, parameters, filter=self.filter,start=self.start,end=self.end))

class FreqDistResult:
    def __init__(self,api_response):
        self.redacted = api_response['analysis']['redacted']
        self.interactions = api_response['interactions']
        self.unique_authors = api_response['unique_authors']
        self.results = dict()

        for res in api_response['analysis']['results']:
            self.results[res['key']] = { 'interactions': res['interactions'], "unique_authors": res['unique_authors'] }

    def to_dataFrame(self):
        if not self.redacted:
            return pd.DataFrame.from_dict(self.results,orient='index')
        else:
            return None

class TimeSeriesResult:
    def __init__(self,api_response):
        self.isRedacted = api_response['analysis']['redacted']
        self.interactions = api_response['interactions']
        self.unique_authors = api_response['unique_authors']
        self.results = dict()

        for res in api_response['analysis']['results']:
            time = datetime.datetime(1970,1,1) + datetime.timedelta(milliseconds=res['key'])
            self.results[time] = { 'interactions': res['interactions'], "unique_authors": res['unique_authors'] }

    def to_dataFrame(self):
        if not self.isRedacted:
            return pd.DataFrame.from_dict(self.results,orient='index')
        else:
            return None

class RecordingInfo:
    def __init__(self,api_response):
        self.start = api_response['start']
        self.end = api_response['end']
        self.hash = api_response['hash']
        self.name = api_response['name']
        self.reached_capacity = api_response['reached_capacity']
        self.remaining_account_capacity = api_response['remaining_account_capacity']
        self.remaining_index_capacity = api_response['remaining_index_capacity']
        self.status = api_response['status']
        self.volume = api_response['volume']