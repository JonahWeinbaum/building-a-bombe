from pyenigma import rotor, enigma
import random
import nltk
nltk.download('words')
from nltk.corpus import words
import string

letters = ''.join(random.choices(string.ascii_uppercase, k=4))
word_list = words.words()

KEY1 = letters[0] + letters[1] + letters[2]
KEY2 = letters[0] + letters[1] + letters[3]

def random_sentence(n=10):
    return ''.join(random.choice(word_list).upper() for _ in range(n))

ROTORS_SET = [
    rotor.ROTOR_I,
    rotor.ROTOR_II,
    rotor.ROTOR_III,
]

rotors = random.sample(ROTORS_SET, k=3)

e1 = enigma.Enigma(rotor.ROTOR_Reflector_B, rotors[0], rotors[1], rotors[2], KEY1, plugs="")
e2 = enigma.Enigma(rotor.ROTOR_Reflector_B, rotors[0], rotors[1], rotors[2], KEY2, plugs="")

text1 = random_sentence(n=10)
text2 = random_sentence(n=10)
etext1 = e1.encipher(text1)
etext2 = e2.encipher(text2)

print()
print(f"Rotor used -> {rotors[2].name}")
print("-"*(abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26) + len(etext2) + 5))
print(f"{KEY1}: {etext1}")
print(f"{KEY2}: " + " "*abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26) + f"{etext2}")
print(f"     " + " "*abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26), end="")
overlap1 = min(len(etext2), len(etext1) - abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26))
coincidences1 = 0
for i in range(overlap1):
    if etext2[i] == etext1[i + abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26)]:
        print("*", end="")
        coincidences1 += 1
    else:
        print(" ", end="")
print()
print("-"*(abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26) + len(etext2) + 5))
if coincidences1 / float(overlap1) > (1/26) + 0.04:
    print(f"No turnover between {KEY1[2]} and {KEY2[2]}")
else:
    print(f"Turnover between {KEY1[2]} and {KEY2[2]}")
print("-"*(abs((ord(KEY2[-1]) - ord(KEY1[-1])) % 26) + len(etext2) + 5))

print()

print("-"*(abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26) + len(etext1) + 5))
print(f"{KEY2}: {etext2}")
print(f"{KEY1}: " + " "*abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26) + f"{etext1}")
print(f"     " + " "*abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26), end="")
overlap2 = min(len(etext1), len(etext2) - abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26))
coincidences2 = 0
for i in range(overlap2):
    if etext1[i] == etext2[i + abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26)]:
        print("*", end="")
        coincidences2 += 1
    else:
        print(" ", end="")
print()
if coincidences2 / float(overlap2) > (1/26) + 0.04:
    print(f"No turnover between {KEY2[2]} and {KEY1[2]}")
else:
    print(f"Turnover between {KEY2[2]} and {KEY1[2]}")

print("-"*(abs((ord(KEY1[-1]) - ord(KEY2[-1])) % 26) + len(etext1) + 5))

