import math


def convert(s):
    L = 10 ** (-28 / 20)
    O = 10 ** (s / 20)
    return math.floor(20 * math.log(O * L - L + 1, 10))


def generate_latex_table():
    # Input scores and their converted values
    raw_scores = list(range(15, 40))
    converted_scores = [convert(s) for s in raw_scores]

    # Start tabular
    latex = "\\begin{tabular}{|c|*{40}{c|}}\n"
    latex += "\\hline\n"

    # Row 1: Raw score
    latex += (
        "Middle-wheel Score & "
        + " & ".join(str(score) for score in raw_scores)
        + " \\\\\n"
    )
    latex += "\\hline\n"

    # Row 2: Converts to
    latex += (
        "End-wheel Score & "
        + " & ".join(str(score) for score in converted_scores)
        + " \\\\\n"
    )
    latex += "\\hline\n"

    # End tabular
    latex += "\\end{tabular}"

    return latex


print(generate_latex_table())
