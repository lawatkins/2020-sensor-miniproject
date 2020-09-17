# Miniproject Report -- Anirudh Watturkar and Luisa Watkins

## Intro/Task 0
---

The purpose of this project is to simulate the data gathering and analysis process in a hardware system communicating with many sensors. The first step in accomplishing this was to set an environment capable of running python websockets and the given simulator code. Upon establishing a connection between the server and the client, the following greeting string is issued by the server to the client:
![ECE Capstone IoT simulator](images/message.jpg)

## Task 1

In this portion, we were tasked to implement File I/O to write the JSON data received by the client to a log file. To do this, we open the log file at the specified path, and each iteration that data is received, we write it to the log file after it is printed to the terminal. Upon receiving any exception, the file is closed. This program was then run for about 30 minutes to generate a sufficiently large dataset for analysis in the next task.

## Task 2

In this section we perform an analysis of the data we gathered in the previous part. The code for the analysis is in analyze.py, which reads in the JSON-formatted log file. We first started by familiarizing ourselves with the existing dictionary that stored the sensor data per each location. Then, we extracted the sensor data (temperature, occupancy, cO2) for each location, and got the summary statistics for each (mean, median, variance). We also plotted normalized histograms for each sensor and location to get a sense of the distribution of the data for each sensor type. For the purpose of this report, we have chosen to highlight **insert location here**

1. From the observed temperature data for class1, the median is 26.9886685610252 and the variance is 141.80997816911497.
2. From the observed occupancy data for class1, the median is 19.0 and the variance is 19.350402127930156.
3. **insert location here**
4. For the time interval of the sensor readings, the mean is 0.5884198516828294 and the variance is 0.9193068585220546. Yes, this time interval histogram does mimic a well-known distribution--the Erlang distribution.

## Task 3

## Task 4


# poisson distribution for the number of times an event occurs in
# an interval of time or space

# Note that if events occur over time and the time between occurrences
# follows an exponential then the number that occur in a time period
# follows a Poisson.
