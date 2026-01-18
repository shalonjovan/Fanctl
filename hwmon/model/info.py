from hwmon.utils.fs import read_str
from hwmon.utils.proc import parse_cpuinfo, parse_meminfo


# ---------- SYSTEM ----------

def get_system_product_name() -> str:
   
    return read_str("/sys/class/dmi/id/product_name")


# ---------- CPU ----------

def get_cpu_info() -> dict:
    
    cpu = parse_cpuinfo()

    return {
        "model_name": cpu.get("model name", ""),
        "architecture": "x86_64",  # implied for modern Intel/AMD
        "cores": int(cpu.get("cpu cores", 0)),
        "processors": int(cpu.get("siblings", 0)),
    }


# ---------- MEMORY ----------

def get_total_ram_mb() -> int:
 
    mem = parse_meminfo()
    return mem.get("MemTotal", 0) // 1024
