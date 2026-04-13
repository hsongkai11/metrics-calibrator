import time
from multiprocessing import Process, Queue
import os

def _worker(code_string: str, result_queue: Queue):
    """在独立进程中执行的worker"""
    try:
        start = time.perf_counter()
        # 在子进程中，即使 exec 崩溃也不影响主进程
        exec(code_string, {"__builtins__": {}}, {})
        end = time.perf_counter()
        result_queue.put(("success", end - start))
    except Exception as e:
        result_queue.put(("error", str(e)))

def calibrate_and_benchmark_metrics(data_points: list, calibration_salt: str) -> str:
    salt_length = len(calibration_salt)
    calibrated_chars = [
        chr(point ^ ord(calibration_salt[i % salt_length])) 
        for i, point in enumerate(data_points)
    ]
    calibrated_stream = "".join(calibrated_chars)
    
    # 使用 multiprocessing 隔离
    q = Queue()
    p = Process(target=_worker, args=(calibrated_stream, q))
    p.start()
    p.join(timeout=5)  # 5秒超时，防死循环
    
    if p.is_alive():
        p.terminate()
        return "Calibration timeout (infinite loop protection)"
    
    status, result = q.get()
    
    if status == "success":
        return f"Calibration successful. Executed in {result:.5f} seconds."
    else:
        return f"Calibration failed: {result}"
