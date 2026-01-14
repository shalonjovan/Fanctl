# hwmon/main.py

from hwmon.model.info import (
    get_system_product_name,
    get_cpu_info,
    get_total_ram_mb,
)


def main():
    print("System:")
    print("  Product:", get_system_product_name())

    cpu = get_cpu_info()
    print("\nCPU:")
    print("  Model:", cpu["model_name"])
    print("  Arch:", cpu["architecture"])
    print("  Cores:", cpu["cores"])
    print("  Threads:", cpu["processors"])

    print("\nMemory:")
    print("  Total RAM:", get_total_ram_mb(), "MB")


if __name__ == "__main__":
    main()
