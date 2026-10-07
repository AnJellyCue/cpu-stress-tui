# CPU Stress TUI

A small, interactive terminal UI for running randomized CPU stress tests on Linux.

Built with [Textual](https://textual.textualize.io/) and Python.

The goal is simple: instead of manually changing CPU stress levels, `cpu-stress-tui` randomly selects different CPU worker counts and runs each test for five minutes while displaying live system information.

## Features

- 🖥️ Detects available CPU threads automatically
- 🎲 Randomly selects CPU stress levels
- ⏱️ Five-minute tests
- 📊 Live CPU utilization
- 🌡️ CPU temperature monitoring when available
- 📈 Test progress bar and countdown
- 📜 Test history
- ⏸️ Pause/stop controls
- 🔄 Randomise the next test
- 🛑 Safely terminates stress processes
- 🧹 Cleans up child processes when exiting
- 🖥️ Fully terminal-based UI

## Stress Levels

The test randomly selects from a set of CPU worker counts based on the number of CPU threads available.

Typical levels include:

- 1 thread
- 2 threads
- 4 threads
- 8 threads
- Half of available CPU threads
- CPU threads minus 4
- All available CPU threads

Duplicate values are automatically removed on systems with fewer CPU threads.

## Requirements

- Linux
- Python 3
- `stress`
- Python packages:
  - `textual`
  - `psutil`

## Installation

Clone the repository:

```bash
git clone https://github.com/AnJellyCue/cpu-stress-tui.git
cd cpu-stress-tui
