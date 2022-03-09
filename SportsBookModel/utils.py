# https://www.anyscale.com/blog/parallelizing-python-code
import math
import numpy as np
from timebudget import timebudget
from multiprocessing import Pool
import os
import pandas as pd

import ray


print("Number of CPUs in the system: {}".format(os.cpu_count()))
iterations_count = round(1e7)


@ray.remote
def complex_operation(input_index):
    print("Complex operation. Input index: {:2d}".format(input_index))

    [math.exp(i) * math.sinh(i) for i in [1] * iterations_count]


@ray.remote
def complex_operation_numpy(input_index):
    print("Complex operation (numpy). Input index: {:2d}".format(input_index))

    data = np.ones(iterations_count)
    np.exp(data) * np.sinh(data)


@timebudget
def run_complex_operations(operation, input):

    ray.get([operation.remote(i) for i in input])


ray.init()

input = range(10)
print("Without NumPy")
run_complex_operations(complex_operation, input)
print("NumPy")
run_complex_operations(complex_operation_numpy, input)


def reduce_df_size(df: pd.DataFrame) -> pd.DataFrame:
    ## downcasting loop
    for column in df.columns:

        if df[column].dtypes == "float64":
            df[column] = df.to_numeric(df[column], downcast="float")
        if df[column].dtypes == "int64":
            df[column] = df.to_numeric(df[column], downcast="integer")
        return df


def reduce_memory_usage(df, verbose=True):
    numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2
    if verbose:
        print(
            "Mem. usage decreased to {:.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df
