"""
Simple python script that sends warnings if VRAM usage exceeds limit.

MAX_VRAM_USAGE is maximal acceptable VRAM usage,
if GPU exceeds this limit warning will be displayed,
then for every +VRAM_THRESHOLD Mib it will display another warning

VRAM_TOTAL is your gpu VRAM capacity. Make sure to update this variable
"""

import subprocess
import re
import time
import sys
import argparse

import logger as l

# max acceptable VRAM usage in megabytes
MAX_VRAM_USAGE = 1900

# VRAM usage threshold in megabytes
VRAM_THRESHOLD = 100

# max available VRAM
VRAM_TOTAL = 2048

# max acceptable temperature in degrees Celcius, work in progress
MAX_TEMP = 80

# temperature threshold in degrees celcius
TEMP_THRESHOLD = 5

# time between updates in seconds
WAITTIME = 2


def _call_function(func, *args, **kwargs):
    """
    Used to call different functions
    """
    if callable(func):
        return func(*args, **kwargs)
    return None


def _update_variables():
    """
    automatically updates variables based on gathered info
    """
    l.log_inf("Attempting to autodetect necessary info...")
    try:
        output = subprocess.check_output(["nvidia-smi",
                                          "--query-gpu=name",
                                          "--format=csv,noheader"])
        l.log_inf(f"Detected GPU: {output.decode('utf-8').strip()}", 1)

        output = subprocess.check_output(["nvidia-smi",
                                          "--query-gpu=memory.total",
                                          "--format=csv,noheader,nounits"])

        global VRAM_TOTAL # pylint: disable=global-statement
        VRAM_TOTAL = int(output.decode("utf-8").strip())
        l.log_inf(f"Detected {VRAM_TOTAL}Mib of VRAM available.", 1)

        global MAX_VRAM_USAGE # pylint: disable=global-statement
        MAX_VRAM_USAGE = VRAM_TOTAL * .9
        l.log_inf(f"MAX_VRAM_USAGE set to {VRAM_TOTAL * .9}", 1)

        l.log_inf(f"Script will update every {WAITTIME}s", 1)

        l.log_inf(f"Max acceptable temperature is set to {MAX_TEMP}°C", 1)

    except subprocess.CalledProcessError as e:
        l.log_err(f"Failed to gather necessary info due to following errors: {e}", 1)

    except FileNotFoundError:
        l.log_err("Failed to gather necessary info, make sure that nvidia drivers are installed!", 1)
        sys.exit()


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
        l.log_err(f"Failed to get VRAM usage! {e}")
        sys.exit()

    except FileNotFoundError:
        l.log_err("Failed to get VRAM usage! " +
                "'nvidia-smi' command not found. " +
                "Please make sure NVIDIA drivers are installed.")
        sys.exit()


def get_temp():
    """
    returns GPU temperature in degrees celcius
    """
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"])
        return int(re.search(r'\d+', output.decode('utf-8')).group())
    except subprocess.CalledProcessError as e:
        l.log_err(f"Failed to get GPU temperature! {e}")
        sys.exit()

    except FileNotFoundError:
        l.log_err("Failed to get GPU temperature! " +
                "'nvidia-smi' command not found. " +
                "Please make sure NVIDIA drivers are installed.")
        sys.exit()


def _send_system_warning(message):
    """
    prints VRAM usage warning using notify-send (change your this as needed)
    """
    try:
        l.log_warn(message)
        subprocess.run(["notify-send", "--urgency=critical" ,"Warning!", message], check=True)
    except subprocess.CalledProcessError as e:
        l.log_err(f"Error: {e}")


def main():
    """
    arguments parsing function
    """
    l.set_print_datetime(True)

    parser = argparse.ArgumentParser(description="VRAM monitor for Nvidia GPUs")
    parser.add_argument('command', nargs='?', choices=['start'], help='the command to execute')
    parser.add_argument('-n', '--noauto', action='store_true', help="don't automatically update variables")
    parser.add_argument('-v', '--verbosity', nargs='?', help='set logger verbosity')
    parser.add_argument('-t', '--time', nargs='?', help='Disable showing time for every log entry.')

    args = parser.parse_args()

    autodetect = True

    if args.noauto:
        autodetect = False

    if args.verbosity:
        l.set_verbosity(int(args.verbosity))

    if args.time:
        l.set_print_datetime(False)

    if args.command == 'start':
        start_monitoring(autodetect=autodetect)

    l.log_err("No command to execute!")


def start_monitoring(autodetect = True, func_vram=None, func_temp=None):
    """
    the main program loop,
    monitors vram usage in real time and sends warnings if it exceeds certain limit
    """
    if autodetect:
        _update_variables()
    else:
        l.log_warn("Program will not attempt to gather any information, " +
        "make sure that information provided in the script is correct!")

    last_warning_vram = MAX_VRAM_USAGE
    last_warning_temp = MAX_TEMP
    while True:
        vram_usage = get_vram_usage()
        gpu_temp = get_temp()

        if vram_usage is not None:
            if vram_usage < last_warning_vram - VRAM_THRESHOLD and last_warning_vram >= MAX_VRAM_USAGE:
                last_warning_vram -= VRAM_THRESHOLD

            l.log_inf(f"VRAM Usage: {vram_usage} MiB, temp: {gpu_temp}°C")
            if gpu_temp > last_warning_temp + TEMP_THRESHOLD:
                last_warning_temp = gpu_temp + TEMP_THRESHOLD
                _send_system_warning(f"GPU temperature exceeded {gpu_temp}°C")
                _call_function(func_temp)

            if vram_usage > last_warning_vram + VRAM_THRESHOLD:
                last_warning_vram = vram_usage + VRAM_THRESHOLD
                _send_system_warning("VRAM usage critical! " +
                        f"{vram_usage}/{VRAM_TOTAL}Mib, " +
                        f"({(int)((vram_usage / VRAM_TOTAL) * 100)}%)")
                _call_function(func_vram)

        time.sleep(WAITTIME)


if __name__ == "__main__":
    main()
