# hwmon/main.py

from hwmon.fan_temp.sensors import (
    get_cpu_temps,
    get_battery_info,
    get_nvme_temps,
    get_fans,
)


def main():
    cpu = get_cpu_temps()

    print("CPU:")
    print(f"  Package: {cpu['package']:.1f}°C")
    for core, temp in cpu["cores"].items():
        print(f"  Core {core}: {temp:.1f}°C")

    print("\nNVMe:")
    for k, v in get_nvme_temps().items():
        print(f"  {k}: {v:.1f}°C")

    print("\nFans:")
    for k, v in get_fans().items():
        print(f"  {k}: {v} RPM")

    print("\nBattery:")
    print(get_battery_info())


if __name__ == "__main__":
    main()
