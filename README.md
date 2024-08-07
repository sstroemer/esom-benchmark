# esom-benchmark

_Energy System Optimization Model Benchmark_ suite for comparing different energy system optimization models.

## Notes

This needs "python3-venv", which you may have to install - if you receive an error like this:

> The virtual environment was not created successfully because ensurepip is not
> available.  On Debian/Ubuntu systems, you need to install the python3-venv
> package using the following command.
>
> apt install python3.10-venv
>
> You may need to use sudo with that command.  After installing the python3-venv
> package, recreate your virtual environment

## Models and versions

This contains a description of all models, their versions, and how to construct the necessary raw model files.

### Calliope

[GitHub](https://github.com/calliope-project/calliope)

#### 0.6.10

```shell
python3.10 -m venv tmp_esom_benchmark
source tmp_esom_benchmark/bin/activate

pip install git+https://github.com/calliope-project/calliope.git@aad664ff1202d298e3265cd8994ca5e9a57788e9
python create_model.py -m calliope -v 0.6.10

deactivate
rm -rf tmp_esom_benchmark
```

#### 0.7.0.dev3

```shell
python3.10 -m venv tmp_esom_benchmark
source tmp_esom_benchmark/bin/activate

pip install git+https://github.com/calliope-project/calliope.git@872978dfe3a305c85e0c279925fb794d970bf6bd
python create_model.py -m calliope -v 0.7.0.dev3

deactivate
rm -rf tmp_esom_benchmark
```
