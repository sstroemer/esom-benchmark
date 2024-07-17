import os
import sys
import subprocess
import tempfile
import re
import json


ret = subprocess.check_call(["pip", "install", "gurobipy"])
assert ret == 0, "Failed to install gurobipy"

ret = subprocess.check_call(
    ["pip", "install", "git+https://github.com/calliope-project/calliope.git@aad664ff1202d298e3265cd8994ca5e9a57788e9"]
)
assert ret == 0, "Failed to install package"

ret = subprocess.run(["pip", "show", "calliope"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
assert ret.returncode == 0, "Failed to retrieve package information"

match = re.search(r"Version:\s*(\d+\.\d+\.\d+)", ret.stdout)
assert match.group(1) == "0.6.10", "Version mismatch"

import calliope
import gurobipy

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from util import get_stats, zip_files


def process(model, name: str, descr: dict):
    print("Processing", name)

    _dir_tmp = tempfile.gettempdir()
    _dir_models = "models"

    _meta_base = {
        "source": "calliope",
        "version": "0.6.10",
        "commit": "aad664ff1202d298e3265cd8994ca5e9a57788e9",
    }

    fn_lp = os.path.join(_dir_tmp, f"{name}.LP")
    fn_json = os.path.join(_dir_tmp, f"{name}.json")
    fn_zip = os.path.join(_dir_models, f"{name}.zip")
    model.to_lp(fn_lp)
    model = gurobipy.read(fn_lp)
    model_stats = get_stats(model, _meta_base | {"name": name, "descr": descr})
    json.dump(model_stats, open(fn_json, "w"), indent=4)
    zip_files([fn_lp, fn_json], fn_zip)

# ======================================================================================================================
# :: URBAN SCALE ::
# ======================================================================================================================

process(
    calliope.examples.urban_scale(),
    "calliope_0610_urban_default",
    {"model": "tutorial_urban_scale", "period": "default"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-01"]}}),
    "calliope_0610_urban_T1D",
    {"model": "tutorial_urban_scale", "period": "first day of January"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-07"]}}),
    "calliope_0610_urban_T1W",
    {"model": "tutorial_urban_scale", "period": "first week of January"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-31"]}}),
    "calliope_0610_urban_T1M",
    {"model": "tutorial_urban_scale", "period": "all of January"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-03-31"]}}),
    "calliope_0610_urban_T3M",
    {"model": "tutorial_urban_scale", "period": "January to March"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-06-30"]}}),
    "calliope_0610_urban_T6M",
    {"model": "tutorial_urban_scale", "period": "January to June"},
)

process(
    calliope.examples.urban_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-12-31"]}}),
    "calliope_0610_urban_T1Y",
    {"model": "tutorial_urban_scale", "period": "one full year"},
)

# ======================================================================================================================
# :: NATIONAL SCALE ::
# ======================================================================================================================

process(
    calliope.examples.national_scale(),
    "calliope_0610_national_default",
    {"model": "tutorial_national_scale", "period": "default"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-01"]}}),
    "calliope_0610_national_T1D",
    {"model": "tutorial_national_scale", "period": "first day of January"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-07"]}}),
    "calliope_0610_national_T1W",
    {"model": "tutorial_national_scale", "period": "first week of January"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-01-31"]}}),
    "calliope_0610_national_T1M",
    {"model": "tutorial_national_scale", "period": "all of January"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-03-31"]}}),
    "calliope_0610_national_T3M",
    {"model": "tutorial_national_scale", "period": "January to March"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-06-30"]}}),
    "calliope_0610_national_T6M",
    {"model": "tutorial_national_scale", "period": "January to June"},
)

process(
    calliope.examples.national_scale(override_dict={"model": {"subset_time": ["2005-01-01", "2005-12-31"]}}),
    "calliope_0610_national_T1Y",
    {"model": "tutorial_national_scale", "period": "one full year"},
)

ret = subprocess.check_call(["pip", "uninstall", "-y", "gurobipy"])
assert ret == 0, "Failed to uninstall gurobipy"

ret = subprocess.check_call(["pip", "uninstall", "-y", "calliope"])
assert ret == 0, "Failed to uninstall calliope"
