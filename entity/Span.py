class Span:
    """
    database: histershop-trace
    collection: span
    for each row in span
    """

    def __init__(self, traceID, spanID, operationName, parentSpanID, startTime, duration):
        self.traceID = traceID
        self.spanID = spanID
        self.operationName = operationName
        self.parentSpanID = parentSpanID
        self.startTime = startTime
        self.duration = duration

