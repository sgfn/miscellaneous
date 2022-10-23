from random import randint

def bday_experiment(n, tests=1000):
    overall_successes = 0
    for i in range(tests):
        values = [randint(1, 365) for j in range(n)]
        unique_values = set(values)
        if len(unique_values) < n:
            overall_successes += 1
    return overall_successes/tests

if __name__ == '__main__':
    for i in range(20, 41):
        print(f'n={i} prob={bday_experiment(i)}')