import sensors

def display_fan_speeds():
    sensors.init()

    try:
        found = False

        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if feature.name.startswith("fan"):
                    try:
                        rpm = feature.get_value()
                        print(f"{chip} - {feature.label}: {rpm:.0f} RPM")
                        found = True
                    except sensors.SensorsError:
                        pass

        if not found:
            print("No fan sensors detected.")

    finally:
        sensors.cleanup()


if __name__ == "__main__":
    display_fan_speeds()
