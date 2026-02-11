import pynvml

try:
    pynvml.nvmlInit()
    print("NVML initialized successfully")

    device_count = pynvml.nvmlDeviceGetCount()
    print(f"GPU Count: {device_count}")

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)

        print(f"\nGPU {i}: {name}")
        print(f"  GPU Usage: {util.gpu}%")
        print(f"  Memory Usage: {util.memory}%")
        print(f"  VRAM Used: {mem.used / (1024**2):.2f} MB")
        print(f"  VRAM Total: {mem.total / (1024**2):.2f} MB")

    pynvml.nvmlShutdown()

except pynvml.NVMLError as err:
    print("NVML Error:", err)
