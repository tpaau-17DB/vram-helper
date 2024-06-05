"""
Simple python script that sends warnings about VRAM usage.
Uses notify-send by default

MAX_VRAM_USAGE is maximal acceptable VRAM usage,
if GPU exceeds this limit warning will be displayed,
then for every +TRESHOLD Mib it will display another warning

BUDGET is your gpu VRAM capacity. Make sure to update this variable
"""

import subprocess
import re
import time
import sys

# max acceptable VRAM usage in megabytes, make sure to update this variable
MAX_VRAM_USAGE = 3800

# Maximum allowed VRAM usage threshold in megabytes
TRESHOLD = 100

#max aviable VRAM, make sure to update this variable
BUDGET = 4096

#time between updates in seconds
WAITTIME = 2

#controls the minimum priority of log messages:
#  -0 to display all logs
#  -1 to display only warnings
#  -2 to display only errors
VERBOSITY_LEVEL = 0


def log_mess(message):
    """
    prints messages in log format
    """
    if VERBOSITY_LEVEL > 0:
        return
    print(f"\033[92m[LOG]\033[0m {message}")


def log_warn(message):
    """
    prints messages in warning format
    """
    if VERBOSITY_LEVEL > 1:
        return
    print(f"\033[33m[WARN]\033[0m {message}")


def log_err(message):
    """
    prints messages in error format
    """
    print(f"\033[91m[ERR]\033[0m {message}")


def get_vram_usage():
    """
    returns main GPU VRAM usage in megabytes
    """
    try:
        output = subprocess.check_output(["nvidia-smi",
                                          "--query-gpu=memory.used",
                                          "--format=csv,noheader,nounits"])
        return int(re.search(r'\d+', output.decode('utf-8')).group())
    except subprocess.CalledProcessError as e:
        log_err(f"Failed to get VRAM usage! {e}")
        sys.exit()
    except FileNotFoundError:
        log_err("Failed to get VRAM usage! " +
                "'nvidia-smi' command not found. " +
                "Please make sure NVIDIA drivers are installed.")
        sys.exit()


def send_vram_warning(message):
    """
    prints VRAM usage warning using notify-send (change your this as needed)
    """
    try:
        print("Warning! " + message)
        subprocess.run(["notify-send", "--urgency=critical" ,"Warning!", message], check=True)
    except subprocess.CalledProcessError as e:
        log_err(f"Error: {e}")


def start_monitoring():
    """
    the main program loop,
    monitors vram usage in real time and sends warnings if it exceeds certain limit
    """
    last_warning_vram = MAX_VRAM_USAGE - 20
    while True:
        vram_usage = get_vram_usage()
        if vram_usage is not None:
            if vram_usage < last_warning_vram - TRESHOLD and last_warning_vram >= MAX_VRAM_USAGE:
                last_warning_vram -= TRESHOLD
            log_mess(f"VRAM Usage: {vram_usage} MiB")
            if vram_usage > last_warning_vram + TRESHOLD:
                last_warning_vram += TRESHOLD
                send_vram_warning("VRAM usage critical! " +
                        f"{vram_usage}/{BUDGET}Mib, " + 
                        f"({(int)((vram_usage / BUDGET) * 100)}%)")
        time.sleep(WAITTIME)


if __name__ == "__main__":
    start_monitoring()
