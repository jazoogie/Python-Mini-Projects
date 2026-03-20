# By Jesse M, ?/03/2026

# A stackable number is one that can be represented in a stack of height >1.
# e.g. 5 is stackable (there are 5 '+'s in the below string)
#  + +
# + + +       (height = 2, [3, 1])

# So is 7:
#  + + +
# + + + +     (height = 2, [4, 2])

# We can prove no power of 2 (i.e. 2^n, n is natural) is stackable.

# This program finds all solutions to stackable numbers, giving the height of the tower
# and the height of the sub-tower that is subtracted from it.


from math import sqrt

def factor_pairs(n):
    pairs = []

    # Note: consider n = 100.
    # going to (sqrt(n) + 1) would yield the factor pair [10, 10].
    # this pair has the same parity - their sum is even - so it can't be used as a pair to
    # determine stackability.
    # this logic follows for any square number. e.g: [5, 5], [7, 7], etc

    # we also skip 1 (for [1, n]), as this always gives us the solution where the stack is 1 high
    for i in range(2, int(sqrt(n))):
        # i is a factor of n
        if (n % i) == 0:
            pairs.append([i, n // i])

    return pairs


def stackable_solutions(n):
    solution_list = []

    n_doubled = n * 2

    # require:
    #   a - b = f1
    #   a + b + 1 = f2

    # =>
    #   2a + 1 = f1 + f2

    fpair_list = factor_pairs(n_doubled)

    for fpair in fpair_list:
        f1, f2 = fpair

        # if the factor pair's sum is even, it can't be useful
        if (f1 + f2) % 2 == 0:
            continue

        a = (f1 + f2 - 1) // 2
        b = a - f1

        solution_list.append([a, b])

    return solution_list


for n in range(1, 129):
    print(n, stackable_solutions(n), sep=" => ")
