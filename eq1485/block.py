import numpy as np
from itertools import permutations

# x = (y . x) . (x . (z . y))
def equation1485(opTable):
	M = len(opTable)
	for x in range(0, M):
		for y in range(0, M):
			for z in range(0, M):
				if(x != opTable[opTable[y][x]][opTable[x][opTable[z][y]]]):
					return False
	return True

def check_submatrices(matrix):
    """ Run checks on the sub-matrices after subdividing the given matrix. """
    M = matrix.shape[0]

    # Check if M is even
    if M % 2 != 0:
        raise ValueError("The size of the matrix must be even.")

    # Determine the midpoints
    mid = M // 2

    # Sub-matrices
    upper_left = matrix[:mid, :mid]
    upper_right = matrix[:mid, mid:]
    bottom_left = matrix[mid:, :mid]
    bottom_right = matrix[mid:, mid:]

    # Check if bottom_left and bottom_right are equal and if upper_left contains only [4, 5, 6, 7] and if bottom_left, bottom_right contain only [0, 1, 2, 3]
    return np.array_equal(bottom_right, bottom_left) and np.all(np.isin(upper_left, [4, 5, 6, 7])) and np.all(np.isin(upper_right, [0, 1, 2, 3])) and np.all(np.isin(bottom_left, [0, 1, 2, 3])) and np.all(np.isin(bottom_right, [0, 1, 2, 3]))

def generate_relabeling_tables(multiplication_table):
    """ Generate all multiplication tables obtained from relabeling a given table. """
    n = len(multiplication_table)
    elements = list(range(n))  # Elements are labeled as 0, 1, ..., n-1
    unique_tables = set()  # Let's avoid duplicates

    # Check all permutations of elements
    for perm in permutations(elements):
        # Create a new multiplication table based on the permutation
        new_table = np.zeros((n, n), dtype=int)

        for i in range(n):
            for j in range(n):
                new_table[perm[i]][perm[j]] = perm[multiplication_table[i][j]]

        # Sanity check - new table still satisfies the equation1485
        # Commenting this line makes the script run faster
        assert(equation1485(new_table))

        # Convert the new table to a tuple of tuples for immutability (easy python hashing)
        unique_tables.add(tuple(map(tuple, new_table)))

    return [np.array(table) for table in unique_tables]

# Example usage:
multiplication_table = np.array(
    [[1, 0, 0, 1, 2, 2, 3, 3],
 [0, 0, 0, 0, 3, 3, 3, 3],
 [4, 4, 4, 4, 5, 5, 5, 5],
 [6, 4, 4, 7, 7, 6, 5, 5],
 [1, 0, 0, 1, 2, 2, 3, 3],
 [6, 4, 4, 7, 7, 6, 5, 5],
 [0, 0, 0, 0, 5, 5, 5, 5],
 [4, 4, 4, 4, 3, 3, 3, 3]])

isomorphic_tables = generate_relabeling_tables(multiplication_table)

for i, table in enumerate(isomorphic_tables):
    if check_submatrices(table):
        # Print all matrices that satisfy check_submatrices()
        print(f"Isomorphic Table {i + 1}:\n{table}\n")
