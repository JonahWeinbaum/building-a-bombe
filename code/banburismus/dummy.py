import math

def score(d1, d2):
    p = (1-d1/100)*(1-d2/100)

    pre_round = 20*math.log(p, 10)
    if pre_round < 0:
        return round(pre_round)
    else:
        return math.floor(pre_round)

def print_latex_table():
    percentages = [i * 5 for i in range(15)]
    
    print(r"\begin{tabular}{c|" + "c" * len(percentages) + "}")
    print(" & " + " & ".join(f"{d2}\\%" for d2 in percentages) + r" \\ \hline")
    
    for d1 in percentages:
        row = [f"{score(d1, d2)}" for d2 in percentages]
        print(f"{d1}\\% & " + " & ".join(row) + r" \\")
    
    print(r"\end{tabular}")
# percentages = [i*5 for i in range(15)]
# for d1 in percentages:
#     for d2 in percentages:
#         print(score(d1, d2), end=" ")
#     print()

print_latex_table()
