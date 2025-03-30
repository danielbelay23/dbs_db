import glob
import os
import numpy as np
import pandas as pd
import pandas_gbq
import datetime as dt
from src.logging import logger
from scipy.stats import norm
from config import PROJECT_ID

this_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = this_dir
data_dir = os.path.join(this_dir, "..", "data")

def load_or_fetch_gbq_df(
    filename_df_pkl="",
    filename_sql="",
    data_dir=data_dir,
    sql_dir=os.path.join(src_dir, "sql"),
    sql_params={},
):
    fname = os.path.join(data_dir, filename_df_pkl)
    if glob.glob(fname):
        df = pd.read_pickle(fname)
        logger.info(f"found {fname} locally.")
    else:
        with open(os.path.join(sql_dir, filename_sql), "r") as f:
            sql = f.read()
        df = pandas_gbq.read_gbq(sql.format(**sql_params), project_id=PROJECT_ID)
        df.to_pickle(fname)
        logger.info(f"{fname} saved to local drive.")

    return df

ALPHA = 0.05


def calc_z_val_p_val(mean_0, mean_1, var_0, var_1, n_0, n_1, n_tests=1):
    """
    Returns:
    --------
    z_val: float
    p_val: float
    critical_alpha: float (adjusted by Bonferroni formula)
    statsig: bool
    """
    pooled_se = np.sqrt(var_1 / n_1 + var_0 / n_0)
    # pooled_se = np.sqrt(var_0 / n_0)
    z_val = abs(mean_1 - mean_0) / pooled_se
    p_val = 2 * norm.sf(z_val)
    critical_alpha = ALPHA / n_tests
    d = dict(
        z_val=z_val,
        p_val=p_val,
        critical_alpha=critical_alpha,
        statsig=bool(p_val < critical_alpha),
    )
    # print(d)
    return pd.Series(d)

def proc_df_statsig(
    df, group="controlled_group", variable="safe_harbor_design", dummy="dc_plan_id"
):
    try:
        g = df.groupby(group)
        n_tests = df[variable].nunique()
        if df[variable].dtype != float and n_tests > 0.2 * df.shape[0]:
            return 1, pd.DataFrame(
                {f"skip calc {variable}": "cardinality too high"}, index=[0]
            )
        mean_0, mean_1 = g[variable].mean().values
        var_0, var_1 = g[variable].var().values
        n_0, n_1 = df.groupby(group)[dummy].count().values
        series = calc_z_val_p_val(mean_0, mean_1, var_0, var_1, n_0, n_1)
        series.name = variable
        return 0, series.to_frame().transpose()

    except TypeError:  # need to calc ratio manually
        g = df.groupby([group, variable])[dummy].count().to_frame("cnt")
        sum_ = g.groupby(level=0).sum().rename(columns={"cnt": "sum"})
        g = g.reset_index().set_index(group).join(sum_)
        g["ratio"] = g["cnt"] / g["sum"]
        g["sd"] = g["ratio"] * (1 - g["ratio"])
        # -- handle each df

        n_tests = g.groupby(variable).ngroups

        if n_tests > 0.2 * df.shape[0]:
            return 1, pd.DataFrame(
                {f"skip calc {variable}": "cardinality too high"}, index=[0]
            )

        def proc_indv_group_pval(small):
            if small.shape[0] != 2:
                return pd.Series(
                    {
                        "z_val": None,
                        "p_val": None,
                        "critical_alpha": None,
                        "statsig": None,
                    }
                )
            g_0, g_1 = small.iloc[0], small.iloc[1]
            mean_0, mean_1 = g_0["ratio"], g_1["ratio"]
            var_0, var_1 = g_0["sd"] ** 2, g_1["sd"] ** 2
            n_0, n_1 = g_0["cnt"], g_1["cnt"]
            return calc_z_val_p_val(
                mean_0, mean_1, var_0, var_1, n_0, n_1, n_tests=n_tests
            )

        return 0, g.groupby(variable).apply(proc_indv_group_pval)


def proc_all_df_statsig_plan_level(df, thresh=0.8):
    variables = df.columns

    out = {}
    out["statsig"] = {}
    out["not statsig"] = {}

    for variable in variables:
        err_code, result = proc_df_statsig(df, variable=variable)
        if err_code == 0:
            statsig_rate = (result.statsig == True).mean()
            if statsig_rate > thresh:
                out["statsig"][variable] = statsig_rate
            else:
                out["not statsig"][variable] = statsig_rate
        else:
            print(result)
    return out
