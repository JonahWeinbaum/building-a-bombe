import math 
def score(n):
    s = 1-(7*6*3)/(8*7*6-5*4*3)
    tau = 1
    if n <= 13:
        tau = s*(26-n)/26 + (1-s)*(13-n)/13
    elif n > 13:
        tau = s*(26-n)/26
    return round(20*math.log(tau, 10))

offsets = list(range(27))
scores = [score(n) for n in offsets]

print(scores)
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
