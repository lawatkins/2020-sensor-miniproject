# Miniproject Report -- Anirudh Watturkar and Luisa Watkins

## Intro/Task 0
---

The purpose of this project is to simulate the data gathering and analysis process in a hardware system communicating with many sensors. The first step in accomplishing this was to set an environment capable of running python websockets and the given simulator code. Upon establishing a connection between the server and the client, the following greeting string is issued by the server to the client:
![ECE Capstone IoT simulator](images/message.jpg)

## Task 1

In this portion, we were tasked to implement File I/O to write the JSON data received by the client to a log file. To do this, we open the log file at the specified path, and each iteration that data is received, we write it to the log file after it is printed to the terminal. Upon receiving any exception, the file is closed. This program was then run for about 30 minutes to generate a sufficiently large dataset for analysis in the next task.

## Task 2

In this section we perform an analysis of the data we gathered in the previous part. The code for the analysis is in analyze.py, which reads in the JSON-formatted log file. We first started by familiarizing ourselves with the existing dictionary that stored the sensor data per each location. Then, we extracted the sensor data (temperature, occupancy, cO2) for each location, and got the summary statistics for each (mean, median, variance). We also plotted normalized histograms for each sensor and location to get a sense of the distribution of the data for each sensor type. For the purpose of this report, we have chosen to highlight the room 'class1':
1. From the observed temperature data for class1, the median is 26.9886685610252 and the variance is 141.80997816911497.
2. From the observed occupancy data for class1, the median is 19.0 and the variance is 19.350402127930156.
3. Temperature Sensor Histogram:
![Temperature Sensor Histogram](images/temperature.jpg)
Occupancy Sensor Histogram:
![Occupancy Sensor Histogram](images/occupancy.jpg)
CO2 Sensor Histogram:
![CO2 Sensor Histogram](images/co2.jpg)
4. For the time interval of the sensor readings, the mean is 0.5884198516828294 and the variance is 0.9193068585220546.
![Time Interval Histogram](images/time_interval.jpg)
Yes, this time interval histogram does mimic a well-known distribution--the Erlang distribution. If we look at what happens within a time interval, we are focusing on how many sensor readings occur. Since this deals with the number of times an event occurs in an interval of time, this follows a Poisson distribution. Since the number of events that occur in a time period follows a Poisson, then the time between occurrences follows an Erlang distribution.

## Task 3

For this task, we took the temperature data from Task 2 and designed and implemented an algorithm to detect anomalies. This is since the temperature variance was larger than expected due to "bad" data values that are unrealistically large and small. We wrote a new function called detect_anomalies and used it within it analyze.py.
1. For the room 'class1', the percent of "bad" data points is 0.02187226596675415, the temperature median with these bad points discarded is 26.989418199038496, and the temperature variance with these bad points discarded is 1.5590970012176244.
2.
3. Possible bounds on temperature for 'office' are: 32.026650 and 16.859730. Possible bounds on temperature for 'class1' are: 37.560409 and 20.007925. Possible bounds on temperature for 'lab1' are: 24.269385 and 18.011436.

## Task 4
