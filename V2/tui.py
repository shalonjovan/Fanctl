from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from pathlib import Path

from state import SystemState


ASSETS = Path(__file__).parent / "assets"


def load_ascii(name: str) -> str:
    return (ASSETS / name).read_text()


def bar(value, max_value, width):
    if max_value == 0:
        return ""
    ratio = min(max(value / max_value, 0), 1)
    filled = int(ratio * width)
    return "█" * filled + " " * (width - filled)


class HwmonTUI(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    #main_container {
        height: 1fr;
        width: 100%;
    }

    #left {
        width: 50%;
        height: 100%;
    }

    #right {
        width: 50%;
        height: 100%;
    }

    #footer {
        height: 1;
        content-align: center middle;
    }

    Static {
        padding: 1;
    }
    """

    terminal_width = reactive(0)

    def on_mount(self):
        self.state = SystemState()
        self.set_interval(1, self.refresh_state)

    def on_resize(self, event):
        self.terminal_width = event.size.width

    def compose(self) -> ComposeResult:
        self.system_info = Static(id="system_info")
        self.fans = Static(id="fans")
        self.cpu_mem = Static(id="cpu_mem")

        left = Vertical(self.system_info, id="left")
        right = Vertical(self.fans, self.cpu_mem, id="right")

        yield Vertical(
            Horizontal(left, right, id="main_container"),
            Static("Hardware Monitor (Reactive Layout)", id="footer")
        )

    def refresh_state(self):
        state = self.state.snapshot()

        # Dynamic bar width based on terminal width
        dynamic_width = max(int(self.terminal_width * 0.15), 10)

        # ================= LEFT =================

        left_text = f"[b]{state['system']['product_name']}[/b]\n"

        for idx, battery in enumerate(state["batteries"], 1):
            left_text += (
                f"\nBattery {idx}\n"
                f"  {battery.get('voltage', 0)} V\n"
                f"  {battery.get('power', 0)} W\n"
            )

        if state["nvme"]:
            left_text += "\nNVMe\n"
            for label, temp in state["nvme"].items():
                left_text += f"  {label}: {temp:.1f}°C\n"

        self.system_info.update(left_text.strip())

        # ================= FANS =================

        fan_text = ""
        for name, rpm in state["fans"].items():
            fan_text += (
                f"{name}: {rpm} RPM\n"
                f"[{bar(rpm, 7600, dynamic_width)}]\n\n"
            )

        self.fans.update(fan_text.strip())

        # ================= CPU / MEMORY =================

        cpu = state["cpu"]
        mem = state["memory"]

        cpu_mem_text = (
            f"CPU\n"
            f"  Temp: {cpu.get('temp', 0) or 0:.1f}°C\n"
            f"  Usage: {cpu['usage_percent']}%\n"
            f"  [{bar(cpu['usage_percent'], 100, dynamic_width)}]\n\n"
            f"Memory\n"
            f"  Used: {mem['used_mb']} MB\n"
            f"  Free: {mem['available_mb']} MB\n"
            f"  [{bar(mem['percent_used'], 100, dynamic_width)}]\n"
        )

        if state["gpu"]:
            cpu_mem_text += "\nGPU\n"
            for name, info in state["gpu"].items():
                cpu_mem_text += (
                    f"  {name}\n"
                    f"    Usage: {info['usage_percent']}%\n"
                    f"    Temp: {info['temp']}°C\n"
                )

        self.cpu_mem.update(cpu_mem_text.strip())


def main():
    HwmonTUI().run()


if __name__ == "__main__":
    main()
