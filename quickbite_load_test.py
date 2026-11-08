import concurrent.futures
import time
import urllib.request
import urllib.error

URL = "http://127.0.0.1:51204/api/orders/orders"
TOTAL_REQUESTS = 5000
WORKERS = 10

def test_request(i):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(URL, timeout=10) as response:
            response.read()
            return response.status, time.perf_counter() - start
    except Exception:
        return 0, time.perf_counter() - start

print("QuickBite Concurrent Load Test Started")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
    results = list(pool.map(test_request, range(TOTAL_REQUESTS)))

duration = time.perf_counter() - start
success = sum(1 for status, _ in results if 200 <= status < 300)
failed = TOTAL_REQUESTS - success

print(f"Total Requests: {TOTAL_REQUESTS}")
print(f"Successful: {success}")
print(f"Failed: {failed}")
print(f"Duration: {duration:.2f} seconds")
print(f"Throughput: {TOTAL_REQUESTS / duration:.2f} requests/sec")
print(f"Average Latency: {sum(t for _, t in results) / len(results) * 1000:.2f} ms")
