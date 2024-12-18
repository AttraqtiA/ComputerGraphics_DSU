import random

# A) Random notes example
chart = []

# Set total duration of the gameplay
total_time = 3.0

# Generate 4 lanes
lanes = [1, 2, 3, 4]

# Generate random notes for the chart with intervals of customizable seconds
for time in [x * 1.0 for x in range(1, int(total_time * 2))]:
    lane = random.choice(lanes)  # Randomly select a lane (1, 2, 3, or 4)
    chart.append({"time": time, "lane": lane})

# B) Manual notes example
chart = [
    {"time": 0.5, "lane": 3},
    {"time": 1.0, "lane": 1},
    {"time": 1.0, "lane": 2},
    {"time": 1.5, "lane": 4},
    {"time": 2.0, "lane": 2},
    {"time": 2.5, "lane": 1},
    {"time": 3.0, "lane": 4},
    {"time": 3.0, "lane": 3},
    {"time": 3.5, "lane": 1},
    {"time": 4.0, "lane": 2},
    {"time": 4.5, "lane": 4},
    {"time": 5.0, "lane": 3},
    {"time": 5.0, "lane": 1},
    {"time": 5.5, "lane": 2},
    {"time": 6.0, "lane": 3},
    {"time": 6.5, "lane": 1},
    {"time": 7.0, "lane": 4},
    {"time": 7.0, "lane": 3},
    {"time": 7.5, "lane": 1},
    {"time": 8.0, "lane": 2},
    {"time": 8.0, "lane": 3},
    {"time": 8.5, "lane": 4},
    {"time": 9.0, "lane": 1},
    {"time": 9.5, "lane": 2},
    {"time": 10.0, "lane": 4},
    {"time": 10.5, "lane": 1},
    {"time": 11.0, "lane": 3},
    {"time": 11.5, "lane": 2},
    {"time": 12.0, "lane": 1},
    {"time": 12.5, "lane": 4},
    {"time": 13.0, "lane": 3},
    {"time": 13.5, "lane": 2},
    {"time": 14.0, "lane": 4},
    {"time": 14.5, "lane": 1},
    {"time": 15.0, "lane": 3},
    {"time": 15.5, "lane": 2},
    {"time": 16.0, "lane": 4},
    {"time": 16.5, "lane": 3},
    {"time": 17.0, "lane": 1},
    {"time": 17.5, "lane": 4},
    {"time": 18.0, "lane": 2},
    {"time": 18.5, "lane": 3},
    {"time": 19.0, "lane": 4},
    {"time": 19.5, "lane": 1},
    {"time": 20.0, "lane": 3}
]

