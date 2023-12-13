class PredictResult(object):
    def __init__(self,
                 name: str,
                 hours: int,
                 minutes: int,
                 seconds: int,
                 score: int | float) -> None:
        self._name = name
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        self._score = score

    @property
    def name(self):
        return self._name
    
    @property
    def hours(self):
        return self._hours
    
    @property
    def minutes(self):
        return self._minutes
    
    @property
    def seconds(self):
        return self._seconds
    
    @property
    def score(self):
        return self._score
    