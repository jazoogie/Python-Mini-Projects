# By Jesse M, 06/07/2023

# A small mini-project to test how different simple prive sieves
# perform.

import time

def time_func(func, inp):
    init_time = time.time()
    func(inp)
    return time.time() - init_time


def primes_to_limit(n):
    if n == 2:
        return [2]
    prime_list = [2, 3]
    if n == 3:
        return prime_list

    k = 6
    while k <= n:
        for j in (k-1, k+1):
            for prime in prime_list:
                if j % prime == 0:
                    break
            else:
                prime_list.append(j)

        k += 6


    return prime_list

def primes_to_limit_fast(n):
    if n == 2:
        return [2]
    prime_list = [2, 3]
    if n == 3:
        return prime_list

    k = 6
    while k <= n:
        for j in (k-1, k+1):
            is_prime = True
            for prime in prime_list:
                if prime ** 2 > j:
                    break
                if j % prime == 0:
                    is_prime = False
                    break

            if is_prime:
                prime_list.append(j)

        k += 6

    return prime_list


val = 100_000

prime_slow = time_func(primes_to_limit, val)
prime_fast = time_func(primes_to_limit_fast, val)

print(f"{prime_slow = :.3f}")
print(f"{prime_fast = :.3f}")
print(f"Diff = {prime_slow - prime_fast:.3f}")
