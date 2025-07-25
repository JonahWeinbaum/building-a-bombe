data = {
    (2, 2): (781.08, 4.99),
    (2, 3): (749.89, 3.58),
    (2, 4): (752.43, 3.43),
    (2, 5): (748.28, 3.46),
    (2, 6): (749.09, 3.42),
    (2, 7): (751.22, 3.47),
    (2, 8): (749.06, 3.42),
    (2, 9): (753.89, 3.58),
    (2, 10): (749.75, 3.56),
    (2, 11): (750.87, 3.49),
    (2, 12): (750.22, 3.57),
    (3, 3): (704.02, 1.73),
    (3, 4): (705.49, 1.75),
    (3, 5): (706.84, 1.69),
    (3, 6): (706.5, 1.78),
    (3, 7): (705.45, 1.68),
    (3, 8): (705.42, 1.7),
    (3, 9): (706.25, 1.69),
    (3, 10): (706.54, 1.69),
    (3, 11): (706.08, 1.62),
    (3, 12): (705.98, 1.7),
    (4, 4): (707.55, 1.63),
    (4, 5): (707.93, 1.59),
    (4, 6): (707.22, 1.6),
    (4, 7): (706.95, 1.58),
    (4, 8): (707.5, 1.66),
    (4, 9): (708.45, 1.65),
    (4, 10): (707.32, 1.63),
    (4, 11): (707.85, 1.66),
    (4, 12): (709.15, 1.62),
    (5, 5): (708.55, 1.65),
    (5, 6): (707.7, 1.61),
    (5, 7): (708.97, 1.61),
    (5, 8): (707.65, 1.65),
    (5, 9): (706.33, 1.59),
    (5, 10): (707.45, 1.66),
    (5, 11): (707.84, 1.68),
    (5, 12): (705.78, 1.57),
    (6, 6): (706.69, 1.59),
    (6, 7): (706.74, 1.61),
    (6, 8): (706.55, 1.66),
    (6, 9): (706.21, 1.6),
    (6, 10): (707.41, 1.57),
    (6, 11): (707.38, 1.62),
    (6, 12): (707.28, 1.66),
    (7, 7): (707.64, 1.61),
    (7, 8): (708.29, 1.56),
    (7, 9): (707.38, 1.6),
    (7, 10): (708.17, 1.6),
    (7, 11): (705.95, 1.58),
    (7, 12): (708.6, 1.58),
    (8, 8): (707.48, 1.63),
    (8, 9): (707.15, 1.59),
    (8, 10): (706.82, 1.66),
    (8, 11): (707.6, 1.61),
    (8, 12): (706.73, 1.61),
    (9, 9): (706.91, 1.64),
    (9, 10): (708.12, 1.64),
    (9, 11): (706.56, 1.57),
    (9, 12): (707.28, 1.6),
    (10, 10): (708.33, 1.62),
    (10, 11): (707.54, 1.58),
    (10, 12): (707.88, 1.61),
    (11, 11): (707.23, 1.63),
    (11, 12): (707.18, 1.62),
    (12, 12): (708.22, 1.6)
}
input_lines = [
    "2 2 781.69",
    "2 3 749.40",
    "2 4 750.42",
    "2 5 751.24",
    "2 6 750.81",
    "2 7 750.08",
    "2 8 750.78",
    "2 9 750.25",
    "2 10 750.05",
    "2 11 750.24",
    "2 12 750.13",
    "3 3 704.13",
    "3 4 705.75",
    "3 5 706.53",
    "3 6 706.12",
    "3 7 705.39",
    "3 8 706.07",
    "3 9 705.55",
    "3 10 705.35",
    "3 11 705.56",
    "3 12 705.40",
    "4 4 707.42",
    "4 5 708.20",
    "4 6 707.79",
    "4 7 707.05",
    "4 8 707.74",
    "4 9 707.21",
    "4 10 707.02",
    "4 11 707.22",
    "4 12 707.07",
    "5 5 708.98",
    "5 6 708.57",
    "5 7 707.83",
    "5 8 708.51",
    "5 9 707.99",
    "5 10 707.80",
    "5 11 708.00",
    "5 12 707.84",
    "6 6 708.16",
    "6 7 707.42",
    "6 8 708.11",
    "6 9 707.59",
    "6 10 707.39",
    "6 11 707.59",
    "6 12 707.44",
    "7 7 706.68",
    "7 8 707.37",
    "7 9 706.85",
    "7 10 706.65",
    "7 11 706.85",
    "7 12 706.70",
    "8 8 708.05",
    "8 9 707.53",
    "8 10 707.33",
    "8 11 707.54",
    "8 12 707.38",
    "9 9 707.01",
    "9 10 706.81",
    "9 11 707.02",
    "9 12 706.86",
    "10 10 706.62",
    "10 11 706.82",
    "10 12 706.67",
    "11 11 707.02",
    "11 12 706.87",
    "12 12 706.72",
]
for line in input_lines:
    i, j, val = line.split()
    i, j = int(i), int(j)
    val = float(val)
    if (i, j) in data:
        mean, error = data[(i, j)]
    elif (j, i) in data:
        mean, error = data[(j, i)]
    else:
        print(f"({i}, {j}) not found in data.")
        continue

    lower, upper = mean - error, mean + error
    status = "within" if lower <= val <= upper else "outside"
    print(f"{i} {j} {val:.2f} is {status} margin [{lower:.2f}, {upper:.2f}]")
