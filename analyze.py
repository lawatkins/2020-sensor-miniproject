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


# function to load data
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

# function for anomaly detection
def detect_anomalies(loc_temp_data, loc, plot=False):
    # This function takes the temperature data for a location and
    # outputs the points that are anomalous
    if plot:
        plt.figure()
        plt.title(loc+" temperature boxplot")

    # Creates a boxplot of the data
    bp = plt.boxplot(loc_temp_data)

    # print("BP med: \n %f\n" % bp['medians'][0].get_ydata()[0])
    # print("BP Whiskers: \n %f, %f\n" %(bp['caps'][0].get_ydata()[0],bp['caps'][1].get_ydata()[0]) )
    # print("\n")

    # Gets the upper and lower whiskers of the data
    bp_top_whisker = bp['caps'][1].get_ydata()[0]
    bp_bottom_whisker = bp['caps'][0].get_ydata()[0]

    # Gets the outlier points above/below the whiskers
    upper_outliers = loc_temp_data[loc_temp_data > bp_top_whisker]
    lower_outliers = loc_temp_data[loc_temp_data < bp_bottom_whisker]

    # print("BP lower outliers: \n")
    # print(np.sort(lower_outliers))
    # print("\n")
    #
    # print("BP upper outliers: \n")
    # print(np.sort(upper_outliers))
    # print("\n")

    if plot:
        plt.figure()
        plt.title(loc+" Boxplot of Upper bound of outliers")

    # Creates boxplot of upper outliers, sets anomalies as upper outliers of upper outliers
    bp_upper = plt.boxplot(upper_outliers)
    upper_anomaly_bound = bp_upper['caps'][1].get_ydata()[0]
    upper_anomalies = loc_temp_data[loc_temp_data > upper_anomaly_bound]

    # print("BP upper anomaly bound: %f\n" %upper_anomaly_bound)
    # print("BP upper anomalies: \n")
    # print(np.sort(upper_anomalies))
    # print("\n")

    if plot:
        plt.figure()
        plt.title(loc+" Boxplot of Lower bound of outliers")

    # Creates boxplot of lower outliers, sets anomalies as lower outliers of lower outliers
    bp_lower = plt.boxplot(lower_outliers)
    lower_anomaly_bound = bp_lower['caps'][0].get_ydata()[0]
    lower_anomalies = loc_temp_data[loc_temp_data < lower_anomaly_bound]

    # print("BP lower anomaly bound: %f\n" %lower_anomaly_bound)
    # print("BP lower anomalies: \n")
    # print(np.sort(lower_anomalies))
    # print("\n")

    if plot:
        plt.show()
    return np.concatenate((lower_anomalies, upper_anomalies), axis=None)

# main function
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()
    data = load_data(file)

    # ******Task 2 - Analysis******
    print('***Room of interest is: class1***\n')
    for k in data:
        print(k.upper())
        # mean
        mean = data[k]['class1'].mean()
        print('mean:')
        print(mean)
        # median
        median = data[k]['class1'].median()
        print("median:")
        print(median)
        # variance
        variance = data[k]['class1'].var()
        print("variance:")
        print(variance)

        # class1
        print("\n")
        temp2 = data[k]["class1"]
        temp2 = temp2[~np.isnan(temp2)]
        temp2 = np.round(temp2)
        val2, counts2 = np.unique(temp2, return_counts=True)
        prob2 = counts2/np.size(temp2)

        plt.figure()
        plt.bar(val2,prob2)
        plt.title("Class1")
        plt.ylabel("Prob( "+k+" )")
        plt.xlabel(k)

    # timing in between readings
    time = data['temperature'].index
    time_interval = np.diff(time.values).astype(np.int64) // 1000000000
    time_mean = np.mean(time_interval)
    time_var = np.var(time_interval)
    print("time interval, mean:")
    print(time_mean)
    print("time interval, variance:")
    print(time_var)

    # print('\nTime Intervals')
    val, counts = np.unique(time_interval, return_counts=True)
    prob = counts/np.size(time_interval)

    # print(time_interval)
    plt.figure()
    plt.bar(val,prob)
    plt.title("Probability of time interval between readings")
    plt.ylabel("Prob( time interval )")
    plt.xlabel("Time interval between readings (seconds)")
    plt.show()

    # ******Task 3 - Anomalies******
    # Gets temperature data
    temperature_data = data["temperature"]
    # Dict to store anomalies indexed by location
    anomalies = {}
    new_data = {}
    # Loops through all locations
    for k in temperature_data:
        loc_temperature_data = temperature_data[k]
        loc_temperature_data = loc_temperature_data[~np.isnan(loc_temperature_data)]
        # Gets anomalies for the temperature data in the current location and stores in dict
        anomalies[k] = detect_anomalies(loc_temperature_data, k)
        intersect, ai, bi = np.intersect1d(loc_temperature_data,anomalies[k],return_indices=True)
        new_data[k] = np.delete(loc_temperature_data.values,ai)
        temperature_data[k] = loc_temperature_data

    original_size = np.size(temperature_data)
    anomaly_size = np.size(anomalies['office']) + np.size(anomalies['class1']) + np.size(anomalies['lab1'])
    bad_data_perc = anomaly_size / original_size
    print('\n\nANOMALY DETECTION (temperature)\n')
    print('percent of bad data points:')
    print(bad_data_perc)

    # values for new data set with anomalies removed
    for k in temperature_data:
        print('\n')
        print("classrooom: "+k)
        # median
        median = np.median(new_data["class1"])
        print("new data's median:")
        print(median)
        # variance
        variance = np.var(new_data['class1'])
        print("new data's variance:")
        print(variance)
