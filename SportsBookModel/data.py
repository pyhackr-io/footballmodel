from typing import Dict, List
import pandas as pd
from urllib.request import urlretrieve
from tqdm import tqdm
import glob
import os
import requests
from zipfile import ZipFile
from io import BytesIO


def load_feature_desc(basedir: str, datadir: str) -> pd.DataFrame:
    """[summary]
    Load data manually cleaned reference data from refdata.csv. This contains all features descriptions to enable context

    Return a dataframe
    """

    print(f"{basedir}{datadir}")
    df_refdata = pd.concat(
        map(pd.read_csv, glob.glob(os.path.join(basedir, f"{datadir}refdata.csv")))
    )
    return df_refdata


def get_datahubio_data(basedir: str, datadir: str, url: str) -> pd.DataFrame:
    """[summary]
    Get data from datahubio and unzip and put data into a datahubio directory.
    Load data and return a dataframe
    """

    r = requests.get(url)
    if r.ok:
        z = ZipFile(BytesIO(r.content))
    print(f"{basedir}{datadir}")
    z.extractall(f"{basedir}{datadir}")
    df = pd.concat(
        map(pd.read_csv, glob.glob(os.path.join(basedir, f"{datadir}/data/*.csv")))
    )

    return df


def get_football_co_uk_data(basedir: str, datadir: str, url: str) -> pd.DataFrame:
    """
    Get data from datahubio and unzip and put data into a datahubio directory.
    Load data and return a dataframe

    return DataFrame
    """
    datadir_fb = os.path.join(basedir, datadir)
    urlretrieve(
        url,
        f"{datadir_fb}2019-2020.csv",
    )[0]
    df_fd = pd.read_csv(f"{basedir}{datadir}2019-2020.csv")

    return df_fd




def merge_df_common_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
        merge football hubio data and football.co.uk data into one data frame where the column
        names are the SAME ONLY for new data frame.

        Need to check if I swap around df1 and df2 there are no issues


        ##### Need to review df1 and df2 logic. As if one has larger number of columns then need to append to dataframe
        #### with larger columns
    """

    fd_list = df1.columns.tolist()
    hubio_list = df2.columns.tolist()
    common_column_list = [i for i in fd_list if i in hubio_list]
    df_merged = pd.DataFrame(df1, columns=fd_list).append(
        pd.DataFrame(df2, columns=common_column_list), ignore_index=True
    )

    return df_merged


def get_df_HTR_FTR_matrix(df: pd.DataFrame) -> Dict[str, float]:
    """[summary]

    Args:
        df (pd.DataFrame): [description]

    Returns:
        [type]: [description]
    """
    results_matrix = (
        df[["HTR", "FTR"]]
        .value_counts(ascending=True)
        .reset_index(name="count")
        .drop(columns="count")
    )
    match_result_matrix = results_matrix["HTR"] + results_matrix["FTR"]
    match_result_matrix.index = match_result_matrix.index + 1

    return {v: k for k, v in match_result_matrix.items()}


def drop_df_columns(df: pd.DataFrame, drop_columns: List[str]) -> pd.DataFrame:

    """[summary]

    Args:
        df (pd.DataFrame): [Frame to drop columns from]
        drop_columns (List): [List of columns to drop]

    Returns:
        pd.DataFrame: [description]
    """
    if len(df) == 0:
        print("DataFrame Empty")
    if len(drop_columns) == 0:
        print("List empty")
    df_updated = df.drop(columns=drop_columns, axis=1)
    return df_updated


def refdata_columnstatus_criteria(
    df_ref: pd.DataFrame, df: pd.DataFrame, colvalue: str
) -> pd.DataFrame:
    """[summary]

    Args:
        df (pd.DataFrame): [Dataframe with all the column information]
        ColumnTypeValue (str): [Value of Column type to match]

    Returns:
        pd.DataFrame: [Dataframe with columns with "MatchInfo value"]
    """
    df_matchinfo_only = df.copy()
    df_ref.value_counts().nunique()
    keep_columns = list(
        df_ref.loc[df_ref["ColumnStatus"].str.contains("Matchinfo", case=False)][
            "ColumnName"
        ]
    )
    for col in df_matchinfo_only.columns:
        if col not in keep_columns:
            del df_matchinfo_only[col]

    return df_matchinfo_only


def standardise_data(df: pd.DataFrame, colvalue: str) -> pd.DataFrame:
    """
    Args:
        colvalue (str): [description]

    Returns:
        pd.DataFrame: [description]
    """

    df_standarised = df.copy()
    # Split date into year, month and day of week (i.e. Saturday, Sunday etc)

    df_standarised["year"] = pd.DatetimeIndex(df_standarised["Date"]).year
    df_standarised["month"] = pd.DatetimeIndex(df_standarised["Date"]).month
    df_standarised["dayofweek"] = pd.DatetimeIndex(df_standarised["Date"]).dayofweek
    df_standarised(columns=["Date"], inplace=True)

    return df_standarised


def drop_df_missing_data(df: pd.DataFrame, drop_percent: int) -> pd.DataFrame:
    """[summary]

    Args:
        df (pd.DataFrame): [description]
        pecentage (int): [description]

    Returns:
        pd.DataFrame: [description]
    """

    # Pecentage of missing data in columns

    df_dropped_missing = df.copy()
    df_missing_col = pd.DataFrame(
        df_dropped_missing.isnull().sum().sort_values(ascending=False) / len(df_dropped_missing) * 100,
        columns=["percentage"],
    )
    col_drop_list=list(df_missing_col[df_missing_col['percentage'] > drop_percent].index)

    for col in df_dropped_missing.columns:
        if col  in col_drop_list:
            del df_dropped_missing[col]

    return df_dropped_missing



# *****************************************************************************
# I AM NOT USING THE DATA FROM data.world. HOWEVER I HAVE KEPT THE FUNCTION IN
# *****************************************************************************
# # def get_dataworld_data(basedir: str, datadir: str , url : str) -> pd.DataFrame:

#     filetype = "csv"
#     urldict = {
#         "2018-2019": "https://query.data.world/s/v4fhwgn6hypbdg4wctbu6jiaifakxp",
#         "2017-2018": "https://query.data.world/s/5zt47ynce4ufblqbsliludl5eyizkc",
#         "2016-2017": "https://query.data.world/s/fzlebshvipjs532kas2yctcxjzc23y",
#         "2015-2016": "https://query.data.world/s/xjyyuqdqa36uweqxvjzpwrnydjlslf",
#         "2014-2015": "https://query.data.world/s/s7tjy3tkhw5uatmnttarqos3mg33k3",
#     }

#     # get data from fat dat.world
#     for key, value in urldict.items():

#         filename = f"{datadir}{key}.{filetype}"
#         if not os.path.isfile(filename):
#             df = pd.read_csv(value)
#             df.to_csv(filename)
#             print(f"downloading {filename}")
#         else:
#             print(f"Already exists {filename}")

#     df_dw = pd.concat(
#         map(pd.read_csv, glob.glob(os.path.join("", f"{datadir_dw}/*.csv")))
#     )
#     return df_dw
