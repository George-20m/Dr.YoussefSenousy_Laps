# app.py - Flask application for tail latency simulation
from flask import Flask
import time
import random
import statistics

app = Flask(__name__)

# Track request statistics
request_count = 0
latencies = []

@app.route('/')
def hello():
    global request_count, latencies

    # Exponential distribution simulates real-world tail latency
    # Mean delay of 0.1 seconds (100ms)
    delay = random.expovariate(1/0.1)
    time.sleep(delay)

    request_count += 1
    latencies.append(delay)

    return f"Response after {delay:.4f} seconds (Request #{request_count})"

@app.route('/stats')
def stats():
    """View latency statistics"""
    global latencies
    if not latencies:
        return "No requests yet"

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)

    return {
        'count': n,
        'mean': f"{statistics.mean(latencies):.4f}s",
        'median': f"{sorted_latencies[n//2]:.4f}s",
        'p95': f"{sorted_latencies[int(n*0.95)]:.4f}s",
        'p99': f"{sorted_latencies[int(n*0.99)]:.4f}s",
        'min': f"{min(latencies):.4f}s",
        'max': f"{max(latencies):.4f}s"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
