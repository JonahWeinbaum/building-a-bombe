from colorama import Fore, Style, init
from enigma.machine import EnigmaMachine
import itertools
import numpy as np
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEBUG = False
init()

def print_debug(str, end="\n"):
    if DEBUG:
        print(str, end=end)

def and_sheets(sheet1, sheet2):
    if sheet1.shape != sheet2.shape:
        raise ValueError("Sheets must have the same shape for bitwise AND.")

    return np.bitwise_and(sheet1, sheet2)

def colorize_cell(value):
    if value == 0:
        return Fore.RED + Style.BRIGHT + '.' + Style.RESET_ALL
    elif value == 1:
        return Fore.GREEN + Style.BRIGHT + 'O' + Style.RESET_ALL
    else:
        return Fore.YELLOW + Style.BRIGHT + str(value) + Style.RESET_ALL


def shift_sheet(sheet, shift=(0, 0)):
    x_shift, y_shift = shift
    h, w = sheet.shape
    result = np.zeros_like(sheet)

    # Calculate source and destination slicing ranges
    x_src_start = max(0, -x_shift)
    x_src_end   = w - max(0, x_shift)
    y_src_start = max(0, -y_shift)
    y_src_end   = h - max(0, y_shift)

    x_dst_start = max(0, x_shift)
    x_dst_end   = w - max(0, -x_shift)
    y_dst_start = max(0, y_shift)
    y_dst_end   = h - max(0, -y_shift)

    # Perform the shift
    result[y_dst_start:y_dst_end, x_dst_start:x_dst_end] = \
        sheet[y_src_start:y_src_end, x_src_start:x_src_end]

    return result

def escape_latex(s):
    # Escape special LaTeX characters
    return str(s).replace('&', r'\&').replace('%', r'\%').replace('$', r'\$') \
                 .replace('#', r'\#').replace('_', r'\_').replace('{', r'\{') \
                 .replace('}', r'\}').replace('~', r'\textasciitilde{}') \
                 .replace('^', r'\^{}').replace('\\', r'\textbackslash{}')
def format_cell(value):
    if value == 0:
        return r'\texttt{.}'
    elif value == 1:
        return r'\texttt{0}'
    else:
        return r'\texttt{' + escape_latex(str(value)) + '}'

def print_sheet_latex(sheet):
    if isinstance(sheet, list):
        sheet = np.array(sheet)

    rows, cols = sheet.shape
    rows = int(rows / 2)
    cols = int(cols / 2)
    col_labels = (ALPHABET)[:cols]
    row_labels = (ALPHABET)[:rows]

    output = []

    # Begin LaTeX tabular
    col_format = 'c|' + 'c' * cols
    output.append(r'\begin{tabular}{' + col_format + '}')
    
    header = ' & ' + ' & '.join(r'\texttt{' + c + '}' for c in col_labels) + r' \\ \hline'
    output.append(header)

    for i in reversed(range(rows)):
        row = [r'\texttt{' + row_labels[i] + '}'] + [format_cell(sheet[i, j]) for j in range(cols)]
        output.append(' & '.join(row) + r' \\')

    output.append(r'\end{tabular}')
    
    print('\n'.join(output))
def print_sheet(sheet):
    if isinstance(sheet, list):
        sheet = np.array(sheet)

    rows, cols = sheet.shape
    col_labels = ALPHABET + ALPHABET
    row_labels = ALPHABET + ALPHABET

    # Print column headers
    header = "   " + " ".join(Fore.CYAN + c + Style.RESET_ALL for c in col_labels)
    print(header)

    for i in reversed(range(rows)):
        label = Fore.MAGENTA + row_labels[i] + Style.RESET_ALL
        row = " ".join(colorize_cell(sheet[i, j]) for j in range(cols))
        print(f"{label}  {row}")
    header = "   " + " ".join(Fore.CYAN + c + Style.RESET_ALL for c in col_labels)
    print(header)

def generate_sheet(rotors="I III II", left_window="A"):
    size = len(ALPHABET)
    sheet = np.zeros((size*2, size*2), dtype=int)

    for x in range(size):
        for y in range(size):
            middle_letter = ALPHABET[x]
            right_letter = ALPHABET[y]
            value = generate_sheet_cell(rotors, left_window + middle_letter + right_letter)

            # Fill all four quadrants

            #HANDLE TURNOVER
            # if ALPHABET[y] in ['B', 'C', 'D', 'E']:
            #     value = 1
            sheet[y,x] = value
            sheet[y+size, x] = value
            sheet[y, x+size] = value
            sheet[y + size, x+ size] = value

    return sheet

def generate_sheet_cell(rotors="I III II", window="AAA"):
    machine_A = EnigmaMachine.from_key_sheet(
       rotors=rotors,
       reflector='B',
       ring_settings=[0,0,0],
       plugboard_settings='')
    starting_pos_A = window
    machine_D = EnigmaMachine.from_key_sheet(
       rotors=rotors,
       reflector='B',
        ring_settings=[0,0,0],
       plugboard_settings='')
    machine_D.set_display(starting_pos_A)
    machine_D.process_text("AAA")
    starting_pos_D = machine_D.get_display()
    machine_A.set_display(starting_pos_A)
    machine_D.set_display(starting_pos_D)


    # decrypt the message key
    perm_A= ['A']*26
    perm_D= ['A']*26
    for i in range(len(ALPHABET)):
        machine_A.set_display(starting_pos_A)
        machine_D.set_display(starting_pos_D)
        perm_A[i] = machine_A.process_text(ALPHABET[i])
        perm_D[i] = machine_D.process_text(ALPHABET[i])
    for i in range(len(ALPHABET)):
        if perm_A[(ord(perm_D[i])-ord('A'))] == chr(ord('A') + i):
            print_debug(starting_pos_A)
            print_debug(starting_pos_D)
            print_debug(f"Permutation D {chr(ord('A') + i)} -> {perm_D[i]}")
            print_debug(perm_D)
            print_debug(f"Permutation A  {perm_D[i]} -> {perm_A[(ord(perm_D[i])-ord('A'))]}")
            print_debug(perm_A)
            print_debug(chr(ord('A') + i))
            return 1

    return 0

SHEETS = {}
for i in range(len(ALPHABET)):
   SHEETS[chr(ord('A') + i)] = (generate_sheet(rotors="I III II", left_window=ALPHABET[i]))

class ZyglaskiSheets:
    def __init__(self):
        size = len(ALPHABET)
        self.sheet = np.ones((size*2, size*2), dtype=int)
        self.zzz_pos = (0,0)

    def next(self, indicator):
        new_sheet = SHEETS[indicator[0]].copy()
        new_zzz = (ord(indicator[1]) - ord('A'), ord(indicator[2]) - ord('A'))
        zzz_shift = (self.zzz_pos[0] - new_zzz[0], self.zzz_pos[1] - new_zzz[1])
        new_sheet_shifted = shift_sheet(new_sheet, zzz_shift)
        old_sheet = self.sheet.copy()
        self.sheet = and_sheets(old_sheet, new_sheet_shifted)

print_sheet_latex(SHEETS['B'])
# for i in range(26):
#     if (chr(-i%26 + ord('A'))) == 'D':
#         zs = ZyglaskiSheets()
#         trigrams = ["BWY", "AFQ", "LZX", "MHX", "RHT", "NSY", "QBW", "SBW", "VFS", "WFW", "YKW"]
# #        trigrams  = ["PTJ", "BSU", "EON", "XLV", "CEH", "BWY", "AGY", "KGS", "XET", "CWI", "CEH", "BUG"]
#         for tg in trigrams:
#             tg = chr(ord('A') + (ord(tg[0])-ord('A')+i) % 26) + tg[1:]

#             zs.next(tg)
#         print_sheet(zs.sheet)
