#!/bin/bash

for a in {2..12}; do
    echo -n "$a "
    for i in {1..100}; do
      echo "./bombe.exe -nodiag <(python3 prob_crib.py --L $a 1) \$(python3 prob_rotor.py) | wc -l"
    done | parallel -j100 > results.txt && python3 mean_moe.py
done
