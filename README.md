# vram-helper
git repo: https://github.com/NicholasNDev/vram-helper

Little python script that displays warning when VRAM exceeds specified limit. Useful when doing some VRAM-intensive tasks on low-end devices (nvidia gpus only).

## Dependencies
  Script requires nvidia-smi to get VRAM usage so you obviously need that installed

  For python requirements you can run:

  ```
  pip install -r requirements.txt
  ```

  Script will send notifications using notify-send, so make sure it works and is configured properly. You can do this by typing:

  ```
  notify-send -u normal "It works?"
  ```

  in your terminal - this should send notification that says "It works"

## Running
  With nvidia-smi and other requirements installed you can run the script by typing:

  ```
  python3 vram-helper.py
  ```

  The script should start printing current vram usage

  Please make sure to adjust settings inside the script - it does not automatically detect your GPU VRAM capacity

## Using
  When doing some vram-intensive task just run `python3 vram-helper` in another terminal - it will prevent crashes by notifying you about critical vram levels

  You can always make this script run on start, but this can be very annoying when playing games, so I just run it manually
