import string
from enigma.machine import EnigmaMachine
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# set machine initial starting position
def print_sheet(sheet):
    rows = len(sheet)
    cols = len(sheet[0]) if rows > 0 else 0
    col_labels = string.ascii_uppercase[:cols]
    row_labels = string.ascii_uppercase[:rows]

    # Print column headers
    print("   " + " ".join(col_labels))

    # Print rows from top to bottom
    for i in range(rows):
        label = row_labels[i]
        row = " ".join(str(sheet[i][j]) for j in range(cols))
        print(f"{label}  {row}")
    return
def generate_sheet(rotors="I III II", left_window="A"):
    size = len(alphabet)
    sheet = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(len(alphabet)):
        for y in range(len(alphabet)):
            middle_letter = chr(ord('A') + x)
            right_letter = chr(ord('A') + y)
            sheet[y][x] = generate_sheet_cell(rotors, left_window + middle_letter + right_letter)
    return sheet
def generate_sheet_cell(rotors="I III II", window="AAA"):
    machine_A = EnigmaMachine.from_key_sheet(
       rotors=rotors,
       reflector='B',
       ring_settings=[25, 25, 25],
       plugboard_settings='')
    starting_pos_A = window
    machine_D = EnigmaMachine.from_key_sheet(
       rotors=rotors,
       reflector='B',
       ring_settings=[25, 25, 25],
       plugboard_settings='')
    starting_pos_D = window[0] + window[1] + chr((ord(window[2])-ord('A')+3) % 26 + ord('A'))
    machine_A.set_display(starting_pos_A)
    machine_D.set_display(starting_pos_D)

    # decrypt the message key
    perm_A= ['A']*26
    perm_D= ['A']*26
    for i in range(len(alphabet)):
        machine_A.set_display(starting_pos_A)
        machine_D.set_display(starting_pos_D)
        perm_A[i] = machine_A.process_text(alphabet[i])
        perm_D[i] = machine_D.process_text(alphabet[i])
    for i in range(len(alphabet)):
        if perm_A[(ord(perm_D[i])-ord('A'))] == chr(ord('A') + i):
            # print(f"Perm A {perm_A}")
            # print(f"Perm D {perm_D}")
            # print(f"For window setting {starting_pos_A}")
            # print(f"Perm D takes {chr(ord('A') + i)} -> {perm_D[i]}")
            # print(f"Perm A takes {perm_D[i]} -> {perm_A[(ord(perm_D[i])-ord('A'))]}")
            # print(f"Female: {chr(i+ord('A'))}")
            return 1

    return 0
#print(generate_sheet_cell(window=alphabet[ord('P') - ord('A')] + "FA"))
sheet = (generate_sheet(left_window=alphabet[ord('P') - ord('A')]))
print_sheet(sheet)
        

