import random
import sys

rotors = random.sample(["I", "II", "III", "IV", "V", "VI"], 3)


sys.stdout.write(rotors[0] + " " + rotors[1] + " " + rotors[2] + " ")
