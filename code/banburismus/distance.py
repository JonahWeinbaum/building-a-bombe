import math


def score(n):
    s = 1 - (7 * 6 * 3) / (8 * 7 * 6 - 5 * 4 * 3)
    tau = 1
    if n <= 13:
        tau = s * (26 - n) / 26 + (1 - s) * (13 - n) / 13
    elif n > 13:
        tau = s * (26 - n) / 26
    return round(20 * math.log(tau, 10))


def score_left(n):
    s1 = 60 / 276
    s2 = 90 / 276
    s3 = 90 / 276
    s4 = 36 / 276

    t1 = (650 - n) / (650)
    t2 = (325 - n) / (325)
    t3 = (312 - n) / (312)
    t4 = (156 - n) / (156)

    tau = 1
    if n < 156:
        tau = s1 * t1 + s2 * t2 + s3 * t3 + s4 * t4
    elif n >= 156 and n < 312:
        tau = s1 * t1 + s2 * t2 + s3 * t3
    elif n >= 312 and n < 325:
        tau = s1 * t1 + s2 * t2
    else:
        tau = s1 * t1
    return round(20 * math.log(tau, 10))


def generate_latex_table():
    # Start the tabular environment
    latex = "\\begin{tabular}{|c|*{26}{c|}}\n"
    latex += "\\hline\n"

    # Header row: i\j, 0 to 25
    latex += "$i \\backslash j$ & " + " & ".join(str(j) for j in range(26)) + " \\\\\n"
    latex += "\\hline\n"

    # Data rows: i = 0 to 9
    for i in range(10):
        # Compute score_left for each j
        row_values = [str(score_left(26 * i + j)) for j in range(26)]
        # Add row: i label, then values
        latex += f"{i} & " + " & ".join(row_values) + " \\\\\n"
        latex += "\\hline\n"

    # End tabular
    latex += "\\end{tabular}"

    return latex


print(generate_latex_table())

# # LaTeX column spec: 1 left-aligned label + 26 monospaced columns
# column_spec = "|l|" + "|".join(["c"] * 26) + "|"

# print(r"\begin{tabular}{" + column_spec + "}")
# print(r"\hline")

# # Offset row
# print(r"\textbf{Offset} & " + " & ".join(r"\texttt{" + str(n).rjust(3) + "}" for n in offsets) + r" \\")
# print(r"\hline")

# # Score row
# print(r"\textbf{Score} & " + " & ".join(r"\texttt{" + str(s).rjust(3) + "}" for s in scores) + r" \\")
# print(r"\hline")
# print(r"\end{tabular}")
