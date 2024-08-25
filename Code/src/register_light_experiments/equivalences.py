from math import factorial

def cycle_count(cycle_type):
    """Calculate the number of distinct permutations for a given cycle type."""
    total_letters = sum(cycle_type)
    num_permutations = factorial(total_letters)
    for size in cycle_type:
        num_permutations //= factorial(size)
    return num_permutations

def choose(n, k):
    """Calculate binomial coefficient C(n, k)."""
    if k > n or k < 0:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def total_arrangements(cycle_type):
    """Calculates the total arrangements possible for a given cycle type."""
    arrangements = 1
    for cycle_size in cycle_type:
        arrangements *= factorial(cycle_size)
    return arrangements

def calculate_duplicates(cycle_type):
    """Calculates the number of duplicates generated for a given cycle type."""
    # Step 1: Count distinct permutations for the cycle type
    distinct_permutations = cycle_count(cycle_type)

    # Step 2: Total arrangements for cycle selections
    total_elements = sum(cycle_type)
    total_selections = 1
    remaining = total_elements
    
    # Count ways to select elements for each cycle
    for size in sorted(cycle_type):
        total_selections *= choose(remaining, size)
        remaining -= size

    # Total generated permutations considering selections
    total_generated = total_selections * total_arrangements(cycle_type)

    # Calculate duplicates
    duplicates = total_generated - distinct_permutations

    return duplicates

def main():
    # Input cycle type (1, 2, 3)
    cycle_type = [1, 2, 3]  # Example cycle type

    # Calculate duplicates for the cycle type
    duplicates = calculate_duplicates(cycle_type)

    print(f"Number of duplicates for cycle type {cycle_type}: {duplicates}")

if __name__ == "__main__":
    main()
