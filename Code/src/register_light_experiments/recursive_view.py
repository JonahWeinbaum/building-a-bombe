import random

n = 26
loop_size = 7  
steps = 100

def d(x):
    for i, x_i in enumerate(x):
        for j, bit in enumerate(x_i):
            if bit and j < loop_size:
                x[j][i] = 1


def o(a, b):
    for i in range(n):
        a[i] = a[i] or b[i]
        b[i] = a[i] or b[i]
    return a


def random_disjoint_transpositions():
    elements = list(range(n))
    transpositions = []
    random.shuffle(elements)

    for i in range(0, n - 1, 2):
        if i + 1 < n:
            transpositions.append((elements[i], elements[i + 1]))

    # If n is odd, add the last element as a self-loop
    if n % 2 == 1:
        transpositions.append((elements[-1], elements[-1]))

    return transpositions

def t(transpositions, bit_number):

    bits = bit_number.copy()
    # Apply the transpositions to the bits
    for (a, b) in transpositions:
        bits[a], bits[b] = bits[b], bits[a]

    # Construct the new bit number from the transposed bits
    return bits

# Example usage



s = 0
iters = 1000
for k in range(iters):
    x = [[0 for j in range(n)] for i in range(loop_size)]
    y = [[0 for j in range(n)] for i in range(loop_size)]
    z = [[0 for j in range(n)] for i in range(loop_size)]
    f = [random_disjoint_transpositions() for i in range(loop_size)]
    g = [random_disjoint_transpositions() for i in range(loop_size)]
    h = [random_disjoint_transpositions() for i in range(loop_size)]
    x[0][8] = 1
    # y[0][3] = 1

    for i in range(steps):
        for j in range(loop_size):
            # x[0] = z[0]
            o(t(f[j], x[j]), x[(j + 1) % loop_size])
            #d(x)
            # y[0] = x[0]
            o(t(h[j], y[j]), y[(j + 1) % loop_size])
            o(x[0], y[0])
            # z[0] = y[0]
            # o(t(g[j], z[j]), z[(j + 1) % loop_size])
            # d(y)
    

    
    if(sum(x[0]) == 26):
        s += 1

print(s/iters)
