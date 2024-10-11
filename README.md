# vram-helper

git repo: https://github.com/tpaau-17DB/vram-helper.git

Little python script that sends warnings when VRAM exceeds specific limit. Useful when doing VRAM-intensive tasks on low-end devices (nvidia gpus only).

## Dependencies

Script requires nvidia-smi to get VRAM usage so you obviously need to install nvidia drivers.

Program will send a notifications using notify-send, so make sure it works and is configured properly. You can do this by typing:

```
notify-send -u normal "It works"
```

This should send notification that says "It works".

## Installing

To download git repo just type:

```
git clone https://github.com/tpaau-17DB/vram-helper.git
```

Navigate to the repo with `cd`:
```
cd vram-helper
```

and then install using pip:

```
pip install .
```

## Running

With nvidia drivers and other requirements installed you can run the script by typing:

```
python3 vram_helper -v 0 start
```

The script should start printing current VRAM usage.

For options type:

```
python3 vram_helper -h
```

Script should automatically update its variables unless you use the `--noauto` parameter.

## Usage

When running a VRAM-intensive task just run `python3 vram_helper start` in another terminal or as a background process - it will help you prevent crashes by notifying you about critical VRAM levels.
