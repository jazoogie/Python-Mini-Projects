# By Jesse M, ?/?/2024

# This program finds the rational roots for a given polnomial.
# It was made quickly just out of interest of the concept of rational
# root theorem.

def factors(n):
    n = abs(n)
    
    factor_list = []
    for i in range(1, int(n ** .5) + 1):
        if n % i == 0:
            factor_list.append(i)
            
    for f in factor_list[::-1]:
        if n // f != f:
            factor_list.append(n // f)
            
    return factor_list


def rational_roots(coeff_list):
    sol_list = []
    
    for q in factors(coeff_list[-1]):
        for p in factors(coeff_list[0]):
            for parity in [-1, 1]:
                x = q / p * parity
                
                _sum = 0
                for coeff, exp in zip(coeff_list, range(len(coeff_list), 0, -1)):
                    exp = exp - 1

                    _sum = _sum + coeff * x ** exp

                if _sum == 0:
                    sol_list.append(f"{q * parity}/{p}")

    return sol_list


# Example polynomial: 6x^3 - 29x^2 - 6x + 5
# Has solutions: x = -1/2, 1/3, 5

poly = [6, -29, -6, 5]
poly_roots = rational_roots(poly)

print(poly_roots)
