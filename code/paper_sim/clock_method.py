from pyenigma import *
import random
import nltk
nltk.download('words')
from nltk.corpus import words

word_list = words.words()

def random_sentence(n=10):
    return ''.join(random.choice(word_list) for _ in range(n))

ROTORS = [
    rotor.ROTOR_I,
    rotor.ROTOR_II,
    rotor.ROTOR_III,
]

# e = enigma.Enigma(reflector, rotors[0], rotors[1], rotors[2], key, plugs="")
# e.encipher("a" * offset)

print(random_sentence(n=15))
