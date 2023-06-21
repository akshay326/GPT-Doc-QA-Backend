from flask import request
from prometheus_client import Counter
from functools import wraps

# Create a counter metric
REQUESTS_TOTAL = Counter('requests_total', 'Total requests.', ['method', 'endpoint', 'client_address'])

def track_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Increment the counter
        REQUESTS_TOTAL.labels(method=request.method, endpoint=request.path, client_address=request.remote_addr).inc()
        return f(*args, **kwargs)
    return decorated_function