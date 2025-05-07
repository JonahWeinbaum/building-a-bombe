import math 
def score(r, l, loss =0):
    p = 10**(loss/20)/17 + (1-10**(loss/20))/26
    bayes_factor = 1
    bayes_factor *= (p)**(r)*(1-p)**(l-r)
    bayes_factor /= (1/26)**(r)*(1-1/26)**(l-r)
    pre_round = 20*math.log(bayes_factor, 10)
    if pre_round < 0:
        return round(pre_round)
    else:
        return math.floor(20*math.log(bayes_factor, 10))

def print_latex_table(loss=0):
    import math

    def score(r, l, loss=0):
        p = 10**(loss/20)/17 + (1 - 10**(loss/20))/26
        bayes_factor = (p)**r * (1 - p)**(l - r)
        bayes_factor /= (1/26)**r * (1 - 1/26)**(l - r)
        pre_round = 20 * math.log(bayes_factor, 10)
        return round(pre_round) if pre_round < 0 else math.floor(pre_round)

    l_values = list(range(40, 64))
    r_values = range(11)

    print(r"\\begin{tabular}{r|" + "r" * len(l_values) + r"}")
    print("& " + " & ".join(str(l) for l in l_values) + r" \\ \hline")

    for r in r_values:
        row = [str(score(r, l, loss=loss)) for l in l_values]
        print(f"{r} & " + " & ".join(row) + r" \\")
    print(r"\end{tabular}")
print_latex_table()
