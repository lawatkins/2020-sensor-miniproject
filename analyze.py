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
        # task 2: analysis
        print(k.upper())
        # median
        median = data[k].median()
        print("median:")
        print(median)
        # variance
        variance = data[k].var()
        print("variance:")
        print(variance)


        # **probability density functions**
        # # office
        # print("\n")
        # print("OFFICE")
        # temp = data[k]["office"]
        # temp = temp[~np.isnan(temp)]
        # temp = np.round(temp)
        # val, counts = np.unique(temp, return_counts=True)
        # prob = counts/np.size(temp)
        #
        # print(temp)
        # print(prob)
        # plt.figure()
        # plt.bar(val,prob)
        # plt.title("Office")
        # plt.ylabel("Prob( "+k+" )")
        # plt.xlabel(k)
        #
        # # class1
        # print("\n")
        # print("CLASS1")
        # temp2 = data[k]["class1"]
        # temp2 = temp2[~np.isnan(temp2)]
        # temp2 = np.round(temp2)
        # val2, counts2 = np.unique(temp2, return_counts=True)
        # prob2 = counts2/np.size(temp2)
        #
        # print(temp2)
        # print(prob2)
        # plt.figure()
        # plt.bar(val2,prob2)
        # plt.title("Class1")
        # plt.ylabel("Prob( "+k+" )")
        # plt.xlabel(k)
        #
        # # lab1
        # print("\n")
        # print("LAB1")
        # temp3 = data[k]["lab1"]
        # temp3 = temp3[~np.isnan(temp3)]
        # temp3 = np.round(temp3)
        # val3, counts3 = np.unique(temp3, return_counts=True)
        # prob3 = counts3/np.size(temp3)
        #
        # print(temp3)
        # plt.figure()
        # plt.bar(val3,prob3)
        # plt.title("Lab1")
        # plt.ylabel("Prob( "+k+" )")
        # plt.xlabel(k)
        print('\n')

    # timing in between readings
    time = data['temperature'].index
    plt.figure()
    plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
    plt.xlabel("Time between readings")
    plt.ylabel("count")
    plt.title("Count of time interval between readings")

    time_interval = np.diff(time.values).astype(np.int64) // 1000000000
    time_med = np.median(time_interval)
    time_var = np.var(time_interval)
    print("time interval, median:")
    print(time_med)
    print("time interval, variance:")
    print(time_var)





    plt.show()
