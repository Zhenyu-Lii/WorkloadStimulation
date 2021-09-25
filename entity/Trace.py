class Trace:
    """
    traceID相同的所有span
    """

    def __init__(self, traceID):
        self.__traceID = traceID
        self.id2span = {}
        self.root_span = None

    def add_span(self, span):
        self.id2span[span.spanID] = span
        if span.parentSpanID == None:
            self.root_span = span




