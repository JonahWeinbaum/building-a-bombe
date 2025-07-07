#!/bin/bash

for a in {9..12}; do
    for b in $(seq $a 12); do
    echo -n "$a $b "
    for i in {1..1000}; do
      echo "./bombe.exe -nodiag <(python3 prob_crib.py --L $a $b) \$(python3 prob_rotor.py) | wc -l"
    done | parallel -j100 > results.txt && python3 mean_moe.py
  done
done
