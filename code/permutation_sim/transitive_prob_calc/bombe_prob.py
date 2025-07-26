from colorama import Fore, Style, init
import argparse
import logging
import pickle

init(autoreset=True)

LOG_FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger("PartitionLogger")


def log_success(message: str):
    logger.info(Fore.GREEN + message)


def log_warning(message: str):
    logger.warning(Fore.YELLOW + message)


def log_error(message: str):
    logger.error(Fore.RED + message)


def log_info(message: str):
    logger.info(Fore.CYAN + message)


def load_cycle_distribution(l: int, enigma: bool) -> dict[tuple[int, ...], float]:
    try:
        log_info("Attempting to load collected cycles cache...")
        if enigma:
            f = open(f"enigmaCycles{l}.dat", "rb")
        else:
            f = open(f"collectedCycles{l}.dat", "rb")
        cycles_d: dict[tuple[int, ...], float] = pickle.load(f)
        f.close()
        return cycles_d
    except:
        log_error("Failed to load collected cycles cache!")
        exit()


def load_transitive_probs() -> (
    dict[tuple[tuple[int, ...], tuple[int, ...], int], float]
):
    try:
        log_info("Attempting to load transitive probability cache...")
        f = open(f"probCache26.dat", "rb")
        transitive_probs: dict[tuple[tuple[int, ...], tuple[int, ...], int], float] = (
            pickle.load(f)
        )
        f.close()
        return transitive_probs
    except:
        log_error("Failed to load transitive probability cache!")
        exit()


def main(l: list[int], c: int, enigma: bool) -> None:
    transitive_probs: dict[tuple[tuple[int, ...], tuple[int, ...], int], faloat] = (
        load_transitive_probs()
    )

    cycle_d1: dict[tuple[int, ...], float] = load_cycle_distribution(l[0], enigma)

    if c == 1:
        prob_stop = 0.0

        for key, val in cycle_d1.items():
            if key != (26,):
                prob_stop += cycle_d1[key]
        log_info(f"Probability of stop with params [l={l}, c={c}] -> {prob_stop:.5f}")
        return
    else:

        cycle_d2: dict[tuple[int, ...], float] = load_cycle_distribution(l[1], enigma)

        prob_stop = 1.0

        for k1, v1 in cycle_d1.items():
            for k2, v2 in cycle_d2.items():

                if k1 == (26,) or k2 == (26,):
                    prob_transitive = 1.0
                else:
                    if ((k1, k2, 26)) in transitive_probs:
                        prob_transitive = transitive_probs[(k1, k2, 26)]
                    elif ((k2, k1, 26)) in transitive_probs:
                        prob_transitive = transitive_probs[(k2, k1, 26)]
                    else:
                        log_error(f"Key error ({k1}, {k2}, 26)")
                        exit()
                prob_k1 = v1
                prob_k2 = v2
                prob_stop -= prob_k1 * prob_k2 * prob_transitive
        log_info(f"Probability of stop with params [l={l}, c={c}] -> {prob_stop:.5f}")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--L",
        type=int,
        default=[10],
        nargs="+",
        help="Number of letters in the menu",
    )

    parser.add_argument(
        "--C",
        type=int,
        default=1,
        help="Number of closures in the menu",
    )

    parser.add_argument('--enigma', action='store_true', help="Use real Enigma for cycle distribution")

    args = parser.parse_args()

    l: list[int] = args.L
    c: int = args.C

    if c == 1 and len(l) == 2:
        c = 2

    if c == 2 and len(l) != 2:
        log_error("Requested two closures but only provided one loop length!")
        exit()

    if c > 2:
        log_error("Support for more than two closures not implemented!")
        exit()

    main(l, c, args.enigma)
