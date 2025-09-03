import time
import pickle
import os
import redis
import statistics
import tempfile

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ITERATIONS = 1000
DATA_SIZE_MB = 1

# Generate dummy data
data = "x" * (DATA_SIZE_MB * 1024 * 1024)
pickled_data = pickle.dumps(data)

def benchmark_redis():
    r = redis.from_url(REDIS_URL)
    r.set("benchmark_key", pickled_data)
    
    times = []
    for _ in range(ITERATIONS):
        start = time.perf_counter()
        _ = r.get("benchmark_key")
        end = time.perf_counter()
        times.append(end - start)
    
    return times

def benchmark_disk():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(pickled_data)
        filepath = f.name
    
    times = []
    for _ in range(ITERATIONS):
        start = time.perf_counter()
        with open(filepath, "rb") as f:
            _ = f.read()
        end = time.perf_counter()
        times.append(end - start)
        
    os.unlink(filepath)
    return times

def run_benchmark():
    print(f"Running benchmark with {DATA_SIZE_MB}MB payload over {ITERATIONS} iterations...")
    
    try:
        redis_times = benchmark_redis()
        disk_times = benchmark_disk()
        
        avg_redis = statistics.mean(redis_times) * 1000  # ms
        avg_disk = statistics.mean(disk_times) * 1000    # ms
        
        print(f"\nResults:")
        print(f"Redis Average Latency: {avg_redis:.4f} ms")
        print(f"Disk  Average Latency: {avg_disk:.4f} ms")
        
        improvement = ((avg_disk - avg_redis) / avg_disk) * 100
        print(f"\nImprovement: {improvement:.2f}% faster")
        
        if improvement > 50:
            print("✅ CLAIM VERIFIED: >50% improvement achieved.")
        else:
            print("⚠️ CLAIM RISK: <50% improvement. Optimization needed.")
            
    except Exception as e:
        print(f"Benchmark failed: {e}")
        print("Ensure Redis is running locally on default port.")

if __name__ == "__main__":
    run_benchmark()
