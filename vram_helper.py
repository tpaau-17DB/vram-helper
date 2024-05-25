"""
Simple python program that sends warnings about vram usage.
Uses mako by default

get_vram_usage() returns vram usage in megabytes

send_vram_warning(message) sends notification to user (using mako by default)

MAX_VRAM_USAGE is maximal acceptable vram usage,
if GPU exceeds this limit warning will be displayed,
then for every +TRESHOLD Mib it will display another warning

BUDGET is your gpu VRAM capacity. Make sure to update this variable
"""

import subprocess
import re
import time

# max acceptable vram usage in megabytes, make sure to update this variable
MAX_VRAM_USAGE = 3800

# Maximum allowed VRAM usage threshold in megabytes
TRESHOLD = 200

#max aviable vram, make sure to update this variable
BUDGET = 4096

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
        print("Error:", e)
        return None

def send_vram_warning(message):
    """
    prints VRAM usage warning using mako (change your notification manager as needed)
    """
    try:
        subprocess.run(["notify-send", "--urgency=critical" ,"Warning!", message])
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == '__main__':
    LAST_WARNING_VRAM = MAX_VRAM_USAGE - TRESHOLD
    while True:
        vram_usage = get_vram_usage()
        if vram_usage is not None:
            if vram_usage < LAST_WARNING_VRAM - TRESHOLD - 20:
                LAST_WARNING_VRAM -= TRESHOLD
            print("VRAM Usage:", vram_usage, "MiB")
            if vram_usage > LAST_WARNING_VRAM + TRESHOLD:
                LAST_WARNING_VRAM += TRESHOLD
                send_vram_warning(f"VRAM usage exceeded {vram_usage}Mib! ({BUDGET - vram_usage}Mib free, {(int)((vram_usage / BUDGET) * 100)}% used)")
        time.sleep(1)
