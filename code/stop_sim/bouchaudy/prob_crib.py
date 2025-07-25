import random
import sys
import argparse


def main(closures):
    total_letters = closures[0] + closures[1] - 1  # Shared letter once
    letters = random.sample(range(26), total_letters)
    letters = [chr(0x41 + x) for x in letters]

    shared = letters[0]
    loop1 = letters[1 : closures[0]] + [shared]  # ends at shared
    loop2 = [shared] + letters[closures[0] :]  # starts at shared

    loop1 = [shared] + loop1  # completes first loop
    loop2 = loop2 + [shared]  # completes second loop

    total_edges = (len(loop1) - 1) + (len(loop2) - 1)
    offsets = random.sample(range(26), total_edges)
    offsets = [chr(0x41 + x) for x in offsets]

    idx = 0
    for i in range(len(loop1) - 1):
        sys.stdout.write(f"ZZ{offsets[idx]}{loop1[i]}{loop1[i+1]}\n")
        idx += 1

    if closures[1] != 1:
       for i in range(len(loop2) - 1):
           sys.stdout.write(f"ZZ{offsets[idx]}{loop2[i]}{loop2[i+1]}\n")
           idx += 1

    sys.stdout.write(f"={shared}=A=\n")
    sys.stdout.write("+++++\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--L",
        type=int,
        nargs=2,
        default=[5, 5],
        help="Lengths of the two closures (must be ≥ 2)",
    )
    args = parser.parse_args()
    main(args.L)
