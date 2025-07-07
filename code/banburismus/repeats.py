GREEN = "\033[92m"
RESET = "\033[0m"

def count_offset_matches(s1, s2, offset):
    s1_aligned, s2_aligned = get_aligned_strings(s1, s2, offset)
    return sum(c1 == c2 for c1, c2 in zip(s1_aligned, s2_aligned))

def get_padded_strings(s1, s2, offset):
    if offset >= 0:
        s1_line = '.' * offset + s1
        s2_line = s2
        length = max(len(s1_line), len(s2_line))
        s1_line = s1_line.ljust(length, '.')
        s2_line = s2_line.ljust(length, '.')
    else:
        s1_line = s1
        s2_line = '.' * (-offset) + s2
        length = max(len(s1_line), len(s2_line))
        s1_line = s1_line.ljust(length, '.')
        s2_line = s2_line.ljust(length, '.')
    return s1_line, s2_line

def print_colored_alignment(s1, s2, offset):
    s1_padded, s2_padded = get_padded_strings(s1, s2, offset)
    s1_colored = []
    s2_colored = []

    for c1, c2 in zip(s1_padded, s2_padded):
        if c1 == c2 and c1 != '.':
            s1_colored.append(GREEN + c1 + RESET)
            s2_colored.append(GREEN + c2 + RESET)
        else:
            s1_colored.append(c1)
            s2_colored.append(c2)

    print("String 1:", "".join(s1_colored))
    print("String 2:", "".join(s2_colored))

s1 = "GXCYBGDSLVWBDJLKWIPEHVYGQZWDTHRQXIKEESQSSPZXARIXEABQIRUCKHGWUEBPF"
s2 = "YNSCFCCPVIPEMSGIZWFLHESCIYSPVRXMCFQAXVXDVUQILBJUABNLKMKDJMENUNQ"

print_colored_alignment(s1, s2, -6)

