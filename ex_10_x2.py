import math

primes = []
counter = 0
check = 3
retrieve = 100

while counter < retrieve - 1:
    sqrt_check = math.sqrt(check)
    is_prime = True

    for prime in primes:
        if prime > sqrt_check:
            break

        if check % prime == 0:
            is_prime = False
            break
        
    if is_prime:
        primes.append(check)
        counter += 1

    check += 2

primes = [2] + primes

print(primes)