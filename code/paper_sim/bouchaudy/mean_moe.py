import math


def mean(data):
    return sum(data) / len(data)


def std_dev(data):
    mean_value = mean(data)
    variance = sum((x - mean_value) ** 2 for x in data) / (
        len(data) - 1
    )  # Sample standard deviation
    return math.sqrt(variance)


# Step 3: Calculate the margin of error
def margin_of_error(data, confidence_level=1.96):
    standard_deviation = std_dev(data)
    n = len(data)
    return confidence_level * (standard_deviation / math.sqrt(n))


def process_file(file_path):
    with open(file_path, "r") as f:
        data = [float(line.strip()) for line in f.readlines()]

    mean_value = mean(data)
    error = margin_of_error(data)

    print(f"{mean_value:.2f} \pm {error:.2f}")


process_file("results.txt")
