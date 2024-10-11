"""
Simple python script that sends warnings about VRAM usage.
Uses notify-send by default
"""

from vram_helper.vram_helper import start_monitoring, get_temp, get_vram_usage
