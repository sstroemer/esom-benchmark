import os
import calliope


end_times = {
    "T24": "2005-01-01 23:00",
    "T168": "2005-01-07 23:00",
    "T730": "2005-01-31 09:00",
    "T2190": "2005-04-02 05:00",
    "T4380": "2005-07-02 11:00",
    "T8760": "2005-12-31 23:00",
}


def run_calliope_0610(path: str):
    """
    ## Calliope v0.6.10

    ```yaml
    meta:
    source: calliope
    version: 0.6.10
    commit: aad664ff1202d298e3265cd8994ca5e9a57788e9
    ```
    """
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(f"{path}/urban_scale"):
        os.mkdir(f"{path}/urban_scale")

    if not os.path.exists(f"{path}/national_scale"):
        os.mkdir(f"{path}/national_scale")

    calliope.examples.urban_scale().to_lp(f"{path}/urban_scale/default.LP")
    calliope.examples.national_scale().to_lp("{path}/national_scale/default.LP")

    for idx in end_times:
        calliope.examples.urban_scale(
            override_dict={
                "model": {"subset_time": ["2005-01-01 00:00", end_times[idx]]}
            }
        ).to_lp(f"{path}/urban_scale/{idx}.LP")

    for idx in end_times:
        calliope.examples.national_scale(
            override_dict={
                "model": {"subset_time": ["2005-01-01 00:00", end_times[idx]]}
            }
        ).to_lp(f"{path}/national_scale/{idx}.LP")


def run_calliope(path: str):
    """
    ## Calliope v0.7.0.dev3

    ```yaml
    meta:
    source: calliope
    version: 0.7.0.dev3
    commit: 872978dfe3a305c85e0c279925fb794d970bf6bd
    ```
    """
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(f"{path}/urban_scale"):
        os.mkdir(f"{path}/urban_scale")

    if not os.path.exists(f"{path}/national_scale"):
        os.mkdir(f"{path}/national_scale")

    def _bnw(model: calliope.Model, path: str):
        model.build()
        model.backend.to_lp(path)

    _bnw(calliope.examples.urban_scale(), f"{path}/urban_scale/default.LP")
    _bnw(calliope.examples.national_scale(), f"{path}/national_scale/default.LP")

    for idx in end_times:
        _bnw(
            calliope.examples.urban_scale(
                override_dict={
                    "config": {"init": {"time_subset": ["2005-01-01", end_times[idx]]}}
                }
            ),
            f"{path}/urban_scale/{idx}.LP",
        )

    for idx in end_times:
        _bnw(
            calliope.examples.national_scale(
                override_dict={
                    "config": {"init": {"time_subset": ["2005-01-01", end_times[idx]]}}
                }
            ),
            f"{path}/national_scale/{idx}.LP",
        )


def run(version: str):
    if version == "0.6.10":
        assert calliope.__version__ == "0.6.10", "Calliope version mismatch."
        run_calliope_0610("out/calliope_0610")
    elif version == "0.7.0.dev3":
        assert calliope.__version__ == "0.7.0.dev3", "Calliope version mismatch."
        run_calliope("out/calliope_070_dev3")
    else:
        raise ValueError(f"Version '{version}' not found for model 'calliope'.")
