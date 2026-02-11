import psutil
import time

def print_system_stats():
    print("===== SYSTEM STATS =====")

    # --- CPU ---
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_per_core = psutil.cpu_percent(percpu=True)
    print(f"\nCPU Usage: {cpu_percent}%")
    print("Per-core:", cpu_per_core)

    # --- RAM ---
    mem = psutil.virtual_memory()
    print(f"\nRAM Usage: {mem.percent}%")
    print(f"Used: {mem.used / (1024**3):.2f} GB")
    print(f"Total: {mem.total / (1024**3):.2f} GB")

    # --- Disk IO ---
    disk_io = psutil.disk_io_counters()
    print("\nDisk IO:")
    print(f"Read: {disk_io.read_bytes / (1024**2):.2f} MB")
    print(f"Write: {disk_io.write_bytes / (1024**2):.2f} MB")

    # --- Network IO ---
    net_io = psutil.net_io_counters()
    print("\nNetwork IO:")
    print(f"Sent: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"Received: {net_io.bytes_recv / (1024**2):.2f} MB")

if __name__ == "__main__":
    print_system_stats()
