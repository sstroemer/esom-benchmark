import os
import zipfile
import gurobipy
import numpy as np
from collections import Counter


def get_raw_stats(model):
    A = model.getA()

    _A_nnz = (A.getnnz(0), A.getnnz(1))
    _A_col_q = np.quantile(_A_nnz[0], [0.90, 0.95, 0.99])
    _A_row_q = np.quantile(_A_nnz[1], [0.90, 0.95, 0.99])
    _A_col_dense = int(sum(_A_nnz[0] >= _A_col_q[-1]))
    _A_row_dense = int(sum(_A_nnz[1] >= _A_row_q[-1]))

    _non_trivial = model.MinBound != 0 or model.MaxBound != 0
    _constr_sense = Counter(model.getAttr("Sense", model.getConstrs()))

    return {
        "size": {
            "variables": {
                "total": model.NumVars,
                "binary": model.NumBinVars,
                "integer": model.NumIntVars,
                "nontrivial_bounds": _non_trivial,
            },
            "constraints": {
                "total": model.NumConstrs,
                "eq": _constr_sense.get("=", 0),
                "le": _constr_sense.get("<", 0),
                "ge": _constr_sense.get(">", 0),
            },
            "nonzeros": model.NumNZs,
        },
        "range": {
            "coefficients": (model.MinCoeff, model.MaxCoeff),
            "rhs": (model.MinRHS, model.MaxRHS),
            "objective": (model.MinObjCoeff, model.MaxObjCoeff),
            "bounds": (model.MinBound, model.MaxBound),
        },
        "sparsity": {
            "columns": {
                "quantiles": _A_col_q.tolist(),
                "num_dense": _A_col_dense,
            },
            "rows": {
                "quantiles": _A_row_q.tolist(),
                "num_dense": _A_row_dense,
            },
        },
    }


def get_stats(model, meta):
    assert not model.IsQP, "QP not supported"
    assert not model.IsQCP, "QCP not supported"

    stats = {
        "meta": meta | {"fingerprint": model.Fingerprint},
        "problem_type": "MILP" if model.IsMIP else "LP",
        "stats": {
            "original": get_raw_stats(model),
            "presolved": [
                {
                    "tool": "gurobi",
                    "version": ".".join([str(it) for it in gurobipy.gurobi().version()]),
                    "stats": get_raw_stats(model.presolve()),
                },
            ],
        },
        "baseline": {
            "solver": "gurobi",
            "version": ".".join([str(it) for it in gurobipy.gurobi().version()]),
        },
    }

    model.setParam("Method", 2)
    model.setParam("Crossover", 0)
    model.setParam("PreDual", 0)
    model.setParam("Seed", 42)

    model.optimize()

    _status_codes = {
        getattr(gurobipy.GRB.Status, attr): attr
        for attr in [it for it in dir(gurobipy.GRB.Status) if not it.startswith("_")]
    }

    stats["baseline"]["solution"] = {
        "solution_status": _status_codes.get(model.Status, "unknown"),
        "runtime": model.Runtime,
        "barrier_iterations": model.BarIterCount,
        "objective_value": model.ObjVal,
    }

    return stats


def zip_files(files: list, fn_zip: str):
    with zipfile.ZipFile(fn_zip, "w") as zf:
        for file in files:
            zf.write(file, arcname=os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
    for file in files:
        os.remove(file)
