"""
Simple python script that sends warnings about vram usage.
Uses mako by default

MAX_VRAM_USAGE is maximal acceptable vram usage,
if GPU exceeds this limit warning will be displayed,
then for every +TRESHOLD Mib it will display another warning

BUDGET is your gpu VRAM capacity. Make sure to update this variable
"""

import subprocess
import re
import time
import sys

# max acceptable vram usage in megabytes, make sure to update this variable
MAX_VRAM_USAGE = 3800

# Maximum allowed VRAM usage threshold in megabytes
TRESHOLD = 100

#max aviable vram, make sure to update this variable
BUDGET = 4096

#time between updates
WAITTIME = 2

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
        print("\033[91m[ERR]\033[0m Failed to get VRAM usage! ", e)
        sys.exit()
    except FileNotFoundError:
        print("\033[91m[ERR]\033[0m Failed to get VRAM usage, 'nvidia-smi' command not found. Make sure NVIDIA drivers are installed.")
        sys.exit();

def send_vram_warning(message):
    """
    prints VRAM usage warning using notify-send (change your this as needed)
    """
    try:
        print("Warning! " + message)
        subprocess.run(["notify-send", "--urgency=critical" ,"Warning!", message])
    except subprocess.CalledProcessError as e:
        print("\033[91m[ERR]\033[0m Error: ", e)

if __name__ == '__main__':
    LAST_WARNING_VRAM = MAX_VRAM_USAGE - 20
    while True:
        vram_usage = get_vram_usage()
        if vram_usage is not None:
            if vram_usage < LAST_WARNING_VRAM - TRESHOLD and LAST_WARNING_VRAM >= MAX_VRAM_USAGE:
                LAST_WARNING_VRAM -= TRESHOLD
            print("\033[92m[LOG]\033[0m VRAM Usage:", vram_usage, "MiB")
            if vram_usage > LAST_WARNING_VRAM + TRESHOLD:
                LAST_WARNING_VRAM += TRESHOLD
                send_vram_warning(f"VRAM usage critical! {vram_usage}/{BUDGET}Mib, ({(int)((vram_usage / BUDGET) * 100)}%)")
        time.sleep(WAITTIME)
