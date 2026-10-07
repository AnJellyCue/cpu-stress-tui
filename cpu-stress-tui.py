#!/usr/bin/env python3

import os
import random
import signal
import subprocess
import time

import psutil
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Label, ProgressBar, Static


DURATION = 300


class CPUStressTUI(App):
    TITLE = "CPU Random Stress"
    SUB_TITLE = "Variable Load Stability Test"

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
        padding: 1 2;
    }

    .panel {
        border: round $accent;
        padding: 1 2;
        margin-bottom: 1;
    }

    #stats {
        height: 10;
    }

    #load {
        height: 8;
    }

    #history {
        height: 1fr;
    }

    .value {
        text-style: bold;
    }

    #status {
        text-style: bold;
    }

    ProgressBar {
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("p", "pause", "Pause"),
        ("s", "stop", "Stop"),
        ("r", "reroll", "Randomise"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()

        self.cores = psutil.cpu_count(logical=True)

        self.loads = [
            1,
            2,
            4,
            8,
            max(1, self.cores // 2),
            max(1, self.cores - 4),
            self.cores,
        ]

        # Remove duplicates and make sure we never exceed available CPUs.
        self.loads = sorted(
            set(min(x, self.cores) for x in self.loads)
        )

        self.cpu_workers = 0
        self.started = 0
        self.process = None
        self.paused = False
        self.running = False
        self.history = []

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="main"):

            with Horizontal(classes="panel", id="stats"):
                yield Static(
                    f"CPU THREADS\n{self.cores}",
                    classes="value",
                )

                yield Static(
                    "STATUS\nStarting...",
                    id="status",
                    classes="value",
                )

                yield Static(
                    "CPU LOAD\n--",
                    id="cpu",
                    classes="value",
                )

                yield Static(
                    "TEMPERATURE\n--",
                    id="temp",
                    classes="value",
                )

            with Vertical(classes="panel", id="load"):
                yield Label("CURRENT TEST")
                yield Label("--", id="current")

                yield ProgressBar(
                    total=DURATION,
                    show_eta=False,
                    id="progress",
                )

                yield Label(
                    "Time remaining: --",
                    id="remaining",
                )

            with Vertical(classes="panel", id="history"):
                yield Label("TEST HISTORY")

                yield Static(
                    "No tests completed yet.",
                    id="history_text",
                )

        yield Footer()

    def on_mount(self):
        self.cpu_timer = self.set_interval(
            1,
            self.update_display,
        )

        self.start_test()

    def start_test(self):
        # Make absolutely sure an old process is gone first.
        self.stop_stress()

        self.cpu_workers = random.choice(self.loads)
        self.started = time.monotonic()
        self.running = True
        self.paused = False

        # Create a separate process group so we can kill stress
        # and all of its worker processes together.
        self.process = subprocess.Popen(
            [
                "stress",
                "--cpu",
                str(self.cpu_workers),
                "--timeout",
                str(DURATION),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        self.query_one("#current", Label).update(
            f"{self.cpu_workers} CPU workers / "
            f"{self.cores} threads"
        )

        self.query_one("#status", Static).update(
            "STATUS\nRUNNING"
        )

        self.query_one("#progress", ProgressBar).update(
            progress=0
        )

    def stop_stress(self):
        """Safely terminate stress and all of its worker processes."""

        if not self.process:
            return

        if self.process.poll() is None:
            try:
                # Kill the entire process group.
                os.killpg(
                    os.getpgid(self.process.pid),
                    signal.SIGTERM,
                )

                self.process.wait(timeout=2)

            except subprocess.TimeoutExpired:
                try:
                    os.killpg(
                        os.getpgid(self.process.pid),
                        signal.SIGKILL,
                    )
                except ProcessLookupError:
                    pass

                try:
                    self.process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass

            except ProcessLookupError:
                pass

        self.process = None

    def update_display(self):
        cpu = psutil.cpu_percent(interval=None)

        self.query_one("#cpu", Static).update(
            f"CPU LOAD\n{cpu:.0f}%"
        )

        try:
            temps = psutil.sensors_temperatures()
            temperature = None

            for entries in temps.values():
                for entry in entries:
                    if entry.current:
                        temperature = entry.current
                        break

                if temperature:
                    break

            if temperature is not None:
                self.query_one("#temp", Static).update(
                    f"TEMPERATURE\n{temperature:.0f}°C"
                )

        except Exception:
            pass

        if not self.running or self.paused:
            return

        elapsed = time.monotonic() - self.started
        remaining = max(0, DURATION - elapsed)

        self.query_one("#progress", ProgressBar).update(
            progress=min(DURATION, elapsed)
        )

        mins = int(remaining // 60)
        secs = int(remaining % 60)

        self.query_one("#remaining", Label).update(
            f"Time remaining: {mins:02d}:{secs:02d}"
        )

        if self.process and self.process.poll() is not None:
            self.finish_test()

    def finish_test(self):
        if not self.running:
            return

        self.running = False
        self.process = None

        timestamp = time.strftime("%H:%M:%S")

        self.history.insert(
            0,
            f"{timestamp}   "
            f"{self.cpu_workers:>3} / "
            f"{self.cores} threads"
        )

        self.history = self.history[:10]

        self.query_one("#history_text", Static).update(
            "\n".join(self.history)
        )

        self.query_one("#status", Static).update(
            "STATUS\nCOMPLETED"
        )

        self.set_timer(
            0.5,
            self.start_test,
        )

    def action_pause(self):
        if not self.running:
            return

        if not self.paused:
            self.stop_stress()

            self.paused = True

            self.query_one("#status", Static).update(
                "STATUS\nPAUSED"
            )

        else:
            self.paused = False
            self.start_test()

    def action_stop(self):
        self.stop_stress()

        self.running = False
        self.paused = False

        self.query_one("#status", Static).update(
            "STATUS\nSTOPPED"
        )

        self.query_one("#current", Label).update(
            "Test stopped"
        )

        self.query_one("#remaining", Label).update(
            "Time remaining: --"
        )

    def action_reroll(self):
        self.stop_stress()
        self.start_test()

    def on_unmount(self):
        """
        Final safety net.

        Called when the Textual application shuts down.
        Ensures stress cannot remain running after the TUI exits.
        """
        self.stop_stress()


if __name__ == "__main__":
    CPUStressTUI().run()
