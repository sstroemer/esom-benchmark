# esom-benchmark

_Energy System Optimization Model Benchmark_ suite for comparing different energy system optimization models.

## Setup

```bash
conda create -n esom-benchmark python=3.11 -y
conda activate esom-benchmark
```

Then run specific files, e.g.:

```bash
python -m ./scripts/calliope_0610.py
```

## Notes

This needs "python3-venv", which you may have to install - if you receive an error like this:

> The virtual environment was not created successfully because ensurepip is not
> available.  On Debian/Ubuntu systems, you need to install the python3-venv
> package using the following command.
>
>     apt install python3.10-venv
>
> You may need to use sudo with that command.  After installing the python3-venv
> package, recreate your virtual environment
