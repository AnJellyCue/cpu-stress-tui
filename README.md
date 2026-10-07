# CPU Stress TUI

> A small interactive terminal UI for running randomized CPU stress tests on Linux.

`cpu-stress-tui` turns a simple CPU stress-testing script into a live Textual TUI. It randomly selects different CPU worker counts, runs each test for five minutes, and displays useful system information while the test is running.

---

## ✨ Features

- 🖥️ Automatic CPU thread detection
- 🎲 Randomized CPU stress levels
- ⏱️ Five-minute stress tests
- 📊 Live CPU utilization
- 🌡️ CPU temperature monitoring when available
- 📈 Live progress bar and countdown
- 📜 Test history
- ⏸️ Pause the current test
- 🛑 Stop the current test
- 🔄 Randomise the next test
- 🧹 Safe cleanup of stress processes
- 🖥️ Fully terminal-based interface

---

## 🔥 How It Works

Each test randomly selects a CPU worker count based on the number of CPU threads available.

Possible loads include:

| Load |
|---|
| 1 thread |
| 2 threads |
| 4 threads |
| 8 threads |
| 50% of CPU threads |
| CPU threads − 4 |
| All CPU threads |

Duplicate values are automatically removed.

Each selected load runs for **5 minutes**, after which another random load is selected.

The process continues until the user stops or exits the application.

---

## 🖥️ Interface

The TUI displays:

- CPU thread count
- Current CPU utilisation
- CPU temperature
- Current stress level
- Test duration
- Remaining time
- Test progress
- Previous test history
- Current application status

---

## 🎮 Controls

| Key | Action |
|---|---|
| `P` | Pause |
| `S` | Stop current test |
| `R` | Randomise / start another test |
| `Q` | Quit |

---

## 📦 Requirements

- Linux
- Python 3
- [`stress`](https://github.com/resurrecting-open-source-projects/stress)
- Python packages:
  - `textual`
  - `psutil`

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/AnJellyCue/cpu-stress-tui.git
cd cpu-stress-tui
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install `stress` if required:

```bash
sudo apt install stress
```

---

## ▶️ Running

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the TUI:

```bash
python3 cpu-stress-tui.py
```

---

## 🛡️ Process Safety

Stress tests intentionally place significant load on the CPU.

You should expect:

- Increased CPU temperature
- Increased power consumption
- Increased fan noise
- Reduced system responsiveness during heavy loads

**Do not run the stress test unattended.**

The application starts stress tests in their own process group and attempts to terminate the entire process group when a test is stopped or the application exits.

This prevents `stress` processes from being accidentally left running after the TUI closes.

---

## 💡 Why I Made It

This project started as a simple Bash script that randomly varied CPU loads for hardware testing.

The script worked perfectly well, but watching terminal output wasn't particularly exciting.

So naturally...

**it became a TUI.** 😄

---

## 🛠️ Technology

Built with:

- **Python**
- **Textual** — terminal user interface
- **psutil** — system and CPU information
- **stress** — CPU stress generation

---

## 📸 Screenshot

_Add a screenshot of the TUI here._

---

## 📄 License

MIT
