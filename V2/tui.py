from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from pathlib import Path

from state import SystemState

ASSETS = Path(__file__).parent / "assets"


def load_ascii(name: str) -> str:
    return (ASSETS / name).read_text()


def bar(value, max_value, width=20, char="█"):
    ratio = min(max(value / max_value, 0), 1)
    filled = int(ratio * width)
    return char * filled + " " * (width - filled)


class HwmonTUI(App):
    CSS_PATH = "tui.tcss"

    def on_mount(self):
        self.state = SystemState()
        self.set_interval(1, self.refresh_state)

    def compose(self) -> ComposeResult:
        pc_ascii = load_ascii("linux.txt")

        self.pc_ascii = Static(pc_ascii, id="pc_ascii")
        self.system_info = Static("", id="system_info")
        self.fans = Static("", id="fans")
        self.cpu_mem = Static("", id="cpu_mem")

        left = Vertical(self.pc_ascii, self.system_info, id="left")
        right = Vertical(self.fans, self.cpu_mem, id="right")

        yield Vertical(
            Horizontal(left, right),
            Static("Hardware Monitor (pysensors + psutil + nvml)", id="footer")
        )

    def refresh_state(self):
        state = self.state.snapshot()

        # ================= LEFT SIDE =================

        left_text = f"[b]{state['system']['product_name']}[/b]\n"

        for idx, battery in enumerate(state["batteries"], 1):
            left_text += (
                f"\nBattery {idx}:\n"
                f"  {battery.get('voltage', 0)} V\n"
                f"  {battery.get('power', 0)} W\n"
            )

        if state["nvme"]:
            left_text += "\nNVMe:\n"
            for label, temp in state["nvme"].items():
                left_text += f"  {label}: {temp:.1f}°C\n"

        self.system_info.update(left_text.strip())

        # ================= RIGHT SIDE =================

        cpu = state["cpu"]
        mem = state["memory"]

        right_text = (
            f"CPU\n"
            f"  Temp: {cpu.get('temp', 0) or 0:.1f}°C\n"
            f"  Usage: {cpu['usage_percent']}%\n"
            f"  [{bar(cpu['usage_percent'], 100)}]\n\n"
            f"Memory\n"
            f"  Used: {mem['used_mb']} MB\n"
            f"  Free: {mem['available_mb']} MB\n"
            f"  [{bar(mem['percent_used'], 100)}]\n"
        )

        if state["gpu"]:
            right_text += "\nGPU\n"
            for name, info in state["gpu"].items():
                right_text += (
                    f"  {name}\n"
                    f"    Usage: {info['usage_percent']}%\n"
                    f"    Temp: {info['temp']}°C\n"
                )

        self.cpu_mem.update(right_text.strip())

        # ================= FANS (ASCII + DATA SIDE BY SIDE) =================

        fan_ascii = load_ascii("fan.txt").splitlines()
        ascii_width = max(len(line) for line in fan_ascii)

        fan_lines = []
        for name, rpm in state["fans"].items():
            fan_lines.append(f"{name}: {rpm} RPM")
            fan_lines.append(f"[{bar(rpm, 7600)}]")
            fan_lines.append("") 


        max_lines = max(len(fan_ascii), len(fan_lines))
        combined_lines = []

        for i in range(max_lines):
            left_part = fan_ascii[i] if i < len(fan_ascii) else ""
            right_part = fan_lines[i] if i < len(fan_lines) else ""

            combined_line = left_part.ljust(ascii_width + 4) + right_part
            combined_lines.append(combined_line)

        self.fans.update("\n".join(combined_lines))


def main():
    HwmonTUI().run()


if __name__ == "__main__":
    main()
