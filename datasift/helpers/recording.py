import datetime

def to_timestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

class PylonRecording(object):
    """Class to represent a Pylon recording"""
    def __init__(self, client, hash):
        self.hash = hash
        self.client = client
        self.analysis = Analysis(self)

    def refresh(self):
        response = self.client.pylon.get(self.hash)
        #Do a get and update the values returned
        for name, value in response.iteritems():
            setattr(self, name, value)

class Analysis(object):
    """A class to hold analysis query parameters and return the queries"""
    def __init__(self, recording):
        self.recording = recording
        self._filter = None
        self._start = None
        self._end = None

    def timeseries(self, interval, span=1):
        response = self.recording.client.pylon.analyze(self.recording.hash, {'analysis_type': 'timeSeries', 'parameters': {'interval': interval, 'span': span}}, self._filter, self._start, self._end)
        timeseries = TimeSeries(response)
        return timeseries

    def freqdist(self, target, threshold=10):
        response = self.recording.client.pylon.analyze(self.recording.hash, {'analysis_type': 'freqDist', 'parameters': {'target': target, 'threshold': threshold}}, self._filter, self._start, self._end)
        freqdist = FreqDist(response)
        return freqdist

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter):
        self._filter = filter

    @filter.deleter
    def filter(self):
        self._filter = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if type(start) is datetime.datetime:
            start = to_timestamp(start)
        if type(start) is not int:
            raise Exception("Start and end must either be a unix time stamp or a datetime object")
        self._start = start

    @start.deleter
    def start(self):
        self._start = None

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if type(end) is datetime.datetime:
            end = to_timestamp(end)
        if type(end) is not int:
            raise Exception("Start and end must either be a unix time stamp or a datetime object")
        self._end = end

    @end.deleter
    def end(self):
        self._end = None

class AnalysisResponse(object):
    def __init__(self, data):
        self.filter = None
        self.redacted = True
        self.parse_response(data)
        self._results

    def parse_response(self, data):
        analysis = dict(data['analysis'])
        data.pop('analysis')
        data.update(analysis)
        for name, value in data.iteritems():
            setattr(self, name, value)

    def get_results(self):
        if self.redacted:
            return dict()
        return self.results

    @property
    def results(self):
        if self.redacted:
            return dict()
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @results.deleter
    def results(self):
        self._results = None

class FreqDist(AnalysisResponse):
    """docstring for FreqDist"""
    pass

class TimeSeries(AnalysisResponse):
    """docstring for TimeSeries"""
    pass


