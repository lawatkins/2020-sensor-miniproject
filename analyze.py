#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    for k in data:
        # data[k].plot()
        time = data[k].index
        # temperature, occupancy, co2
        # data[k].hist()
        # # timing in between readings
        # plt.figure()
        # plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        # plt.xlabel("Time (seconds)")

        # # task 2: analysis
        # print(k.upper())
        # median = data[k].median()
        # variance = data[k].var()
        # time_interval = np.diff(time.values).astype(np.int64) // 1000000000
        # time_med = np.median(time_interval)
        # time_var = np.var(time_interval)
        #
        # # median
        # print("median:")
        # print(median)
        # print("time interval, median:")
        # print(time_med)
        # # variance
        # print("variance:")
        # print(variance)
        # print("time interval, variance:")
        # print(time_var)

        # probability density function
        print("\n")
        print("OFFICE")
        temp = data[k]["office"]
        temp = temp[~np.isnan(temp)]
        print(temp)
        plt.figure()
        temp.hist(density = True, align = "mid")
        plt.title("Office")
        plt.ylabel(k)
        plt.xlabel("Time (in seconds)")

        print("\n")
        print("CLASS1")
        temp2 = data[k]["class1"]
        temp2 = temp2[~np.isnan(temp2)]
        print(temp2)
        plt.figure()
        temp2.hist(density = True, align = "mid")
        plt.title("Class1")
        plt.ylabel(k)
        plt.xlabel("Time (in seconds)")

        print("\n")
        print("LAB1")
        temp3 = data[k]["lab1"]
        temp3 = temp3[~np.isnan(temp3)]
        print(temp3)
        plt.figure()
        temp3.hist(density = True, align = "mid")
        plt.title("Lab1")
        plt.ylabel(k)
        plt.xlabel("Time (in seconds)")








    plt.show()
