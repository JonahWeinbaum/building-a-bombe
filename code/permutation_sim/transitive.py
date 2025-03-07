from itertools import combinations

def partition_of_partition(p1, p2):
        
    def backtrack(p1, p2, index, current_partition, result, seen):
        # We have gone through all targets
        if index == len(p2):

            # No elements remain in p1 thus our partition is valid
            if not p1:

                # Add partition to result only if not seen before
                partition_tuple = tuple(tuple(sorted(sub)) for sub in current_partition)
                if partition_tuple not in seen:
                    seen.add(partition_tuple)
                    result.append(current_partition[:])
            return

        # Next target value in P2
        target = p2[index]

        # Get unique subsets of p1 which add to target value
        for subset in get_unique_subsets_with_sum(p1, target):
           remaining = list(p1)
           for elem in subset:
               remaining.remove(elem)            
           backtrack(remaining, p2, index + 1, current_partition + [list(subset)], result, seen)

    result = []
    seen = set()
    
    backtrack(p1, p2, 0, [], result, seen)
    return result
 
def group_partitions(part1, part2):
    return [[list(a), list(b)] for a, b in zip(part1, part2)]

def get_unique_subsets_with_sum(numbers, target):
    unique_subsets = []
    
    def find_subsets(index, current_subset, current_sum):
        # Reached target
        if current_sum == target:
            if sorted(current_subset) not in [sorted(x) for x in unique_subsets]:
                unique_subsets.append(current_subset.copy())
            return

        # Overshot
        if current_sum > target or index >= len(numbers):
            return
        
        # Include the current number
        current_subset.append(numbers[index])
        find_subsets(index + 1, current_subset, current_sum + numbers[index])
        
        # Exclude the current number
        current_subset.pop()
        find_subsets(index + 1, current_subset, current_sum)
    
    find_subsets(0, [], 0)
    return unique_subsets

