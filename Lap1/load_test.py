# load_test.py - Load testing script for tail latency analysis
import requests
import time
import statistics
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

def make_request(url):
    """Make a single request and return latency"""
    start = time.time()
    try:
        response = requests.get(url)
        latency = time.time() - start
        return latency, response.status_code
    except Exception as e:
        return None, str(e)

def run_load_test(url, num_requests, concurrency):
    """Run load test with specified concurrency"""
    latencies = []
    errors = 0

    print(f"Running {num_requests} requests with {concurrency} concurrent...")

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]

        for future in as_completed(futures):
            latency, result = future.result()
            if latency:
                latencies.append(latency)
            else:
                errors += 1

    return latencies, errors

def plot_latency_histogram(latencies, filename='latency_histogram.png'):
    """Create histogram of latencies"""
    plt.figure(figsize=(12, 6))

    # Main histogram
    plt.subplot(1, 2, 1)
    plt.hist(latencies, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Latency (seconds)')
    plt.ylabel('Frequency')
    plt.title('Latency Distribution')
    plt.axvline(statistics.mean(latencies), color='r', linestyle='--',
                label=f'Mean: {statistics.mean(latencies):.4f}s')
    plt.legend()

    # Tail distribution (sorted)
    plt.subplot(1, 2, 2)
    sorted_latencies = sorted(latencies)
    percentiles = range(0, 101, 1)
    n = len(sorted_latencies)
    values = [sorted_latencies[min(int(n * p / 100), n - 1)] for p in percentiles]

    plt.plot(percentiles, values)
    plt.xlabel('Percentile')
    plt.ylabel('Latency (seconds)')
    plt.title('Latency Percentiles')
    plt.grid(True, alpha=0.3)

    # Mark key percentiles
    for p in [50, 90, 95, 99]:
        idx = int(len(sorted_latencies) * p / 100)
        plt.axvline(p, color='r', linestyle='--', alpha=0.5)
        plt.annotate(f'P{p}: {sorted_latencies[idx]:.4f}s',
                    (p, sorted_latencies[idx]),
                    xytext=(5, 5), textcoords='offset points')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Histogram saved to {filename}")

if __name__ == '__main__':
    URL = 'http://localhost:5000/'

    # Run tests with different concurrency levels
    test_configs = [
        (100, 1),    # Low concurrency
        (100, 10),   # Medium concurrency
        (100, 50),   # High concurrency
    ]

    all_results = {}

    for num_requests, concurrency in test_configs:
        latencies, errors = run_load_test(URL, num_requests, concurrency)

        if latencies:
            sorted_lat = sorted(latencies)
            n = len(sorted_lat)

            print(f"\n{'='*50}")
            print(f"Concurrency: {concurrency}")
            print(f"{'='*50}")
            print(f"Total Requests: {num_requests}")
            print(f"Errors: {errors}")
            print(f"Mean Latency: {statistics.mean(latencies):.4f}s")
            print(f"Median Latency: {sorted_lat[n//2]:.4f}s")
            print(f"P95 Latency: {sorted_lat[int(n*0.95)]:.4f}s")
            print(f"P99 Latency: {sorted_lat[int(n*0.99)]:.4f}s")
            print(f"Min Latency: {min(latencies):.4f}s")
            print(f"Max Latency: {max(latencies):.4f}s")
            print(f"Std Dev: {statistics.stdev(latencies):.4f}s")

            all_results[concurrency] = latencies

    # Plot results
    plot_latency_histogram(all_results[10])

    # Compare concurrency effects
    plt.figure(figsize=(10, 6))
    for concurrency, latencies in all_results.items():
        sorted_lat = sorted(latencies)
        percentiles = range(0, 101, 5)
        n = len(sorted_lat)
        values = [sorted_lat[min(int(n * p / 100), n - 1)] for p in percentiles]
        plt.plot(percentiles, values, label=f'Concurrency={concurrency}')

    plt.xlabel('Percentile')
    plt.ylabel('Latency (seconds)')
    plt.title('Latency vs Concurrency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('latency_vs_concurrency.png', dpi=150)
    print("Concurrency comparison saved to latency_vs_concurrency.png")
