class FixedPrecision:
    def __init__(self, precision: int):
        self.precision = precision
        self.negative = False
        self.entier = 0
        self.mantissa = [0 for _ in range(precision)]
        # unused
        # self.mantissa_first_significant = 0
        # self.mantissa_last_significant = 0

    def print(self):
        if self.negative:
            print('-', end='')
        print(self.entier, end='.')
        print(*self.mantissa, sep='')

    def set(self, string):
        ent, man = string.split('.')
        if ent[0] == '-':
            self.entier = int(ent[1:])
            self.negative = True
        else:
            self.entier = int(ent)
            self.negative = False

        for i, digit in enumerate(man):
            self.mantissa[i] = int(digit)
        
        for i in range(len(man), self.precision):
            self.mantissa[i] = 0

    def div2(self):
        p = self.entier % 2
        self.entier //= 2
        for i, digit in enumerate(self.mantissa):
            r = p * 10 + digit
            p = r % 2
            self.mantissa[i] = r // 2


def fixed_lt(fixed_1: FixedPrecision, fixed_2: FixedPrecision):
    # different signs
    if fixed_1.negative ^ fixed_2.negative:
        return fixed_1.negative
    
    if fixed_1.entier < fixed_2.entier:
        return False if fixed_1.negative else True
    if fixed_1.entier > fixed_2.entier:
        return True if fixed_1.negative else False

    # assuming both numbers have the same precision
    for i in range(fixed_1.precision):
        if fixed_1.mantissa[i] < fixed_2.mantissa[i]:
            return False if fixed_1.negative else True
        if fixed_1.mantissa[i] > fixed_2.mantissa[i]:
            return True if fixed_1.negative else False
    return False


def fixed_nonnegative_diff(fixed_1: FixedPrecision, fixed_2: FixedPrecision):
    # (function works as intended only when fixed_1 >= fixed_2;
    #                                       fixed_1, fixed_2 - nonnegative)

    # assuming both numbers have the same precision
    diff = FixedPrecision(fixed_1.precision)

    # if fixed_1 < fixed_2, swap them around and change the sign
    if fixed_lt(fixed_1, fixed_2):
        fixed_1, fixed_2 = fixed_2, fixed_1
        diff.negative = True

    # manual subtraction
    p = 0
    for i in range(diff.precision-1, -1, -1):
        res = fixed_1.mantissa[i] - fixed_2.mantissa[i] + p
        if res >= 0:
            diff.mantissa[i] = res
            p = 0
        else:
            diff.mantissa[i] = res + 10
            p = -1

    diff.entier = fixed_1.entier - fixed_2.entier + p
    return diff


def fixed_squared(fixed: FixedPrecision):
    squared = FixedPrecision(2 * fixed.precision)
    squared_tab = [0 for _ in range(2 * fixed.precision + 9)]

    fixed_tab = [0 for _ in range(fixed.precision + 5)]
    for i in range(fixed.precision-1, -1, -1):
        fixed_tab[i+5] = fixed.mantissa[i]
    t = fixed.entier
    i = 4
    while t > 0:
        fixed_tab[i] = t % 10
        t //= 10
        i -= 1

    for i in range(fixed.precision+4, -1, -1):
        p = 0
        for j in range(fixed.precision+4, -1, -1):
            res = fixed_tab[i] * fixed_tab[j] + p
            squared_tab[i+j] += res % 10

            p = res // 10 + squared_tab[i+j] // 10
            squared_tab[i+j] %= 10

        if i > 0:
            squared_tab[i-1] += p
    
    ent = 0
    pos = 1
    for i in range(8, -1, -1):
        ent += squared_tab[i] * pos
        pos *= 10
    
    squared.entier = ent
    squared.mantissa = squared_tab[9:].copy()
    return squared
    

def fixed_add_to_fixed(fixed_1: FixedPrecision, fixed_2: FixedPrecision):
    p = 0
    for i in range(fixed_1.precision-1, -1, -1):
        r = fixed_1.mantissa[i] + fixed_2.mantissa[i] + p
        if r >= 10:
            fixed_1.mantissa[i] = r - 10
            p = 1
        else:
            fixed_1.mantissa[i] = r
            p = 0
    fixed_1.entier += fixed_2.entier + p


def sqrt_approx(n: int, m: int):
    approx = FixedPrecision(n)
    step = FixedPrecision(n)
    # 1 <= m <= 10^8; 1 <= n <= 100; m,n natural
    # thus 1 <= sqrt(m) <= 10^4
    # furthermore, 1 <= sqrt(m) <= m
    approx.entier = min(m, 10000)
    approx.div2()
    step.entier = approx.entier
    step.mantissa = approx.mantissa.copy()

    # Will approximate the square root using binsearch
    # Caution: last digit may not be correct
    while True:
        step.div2()
        prod = fixed_squared(approx)
        if step.entier == 0 and max(step.mantissa) == 0: # far from optimal
            break
        if prod.entier - m == 0 and max(prod.mantissa) == 0:
            break
        if prod.entier - m < 0:
            # increase the approximation
            fixed_add_to_fixed(approx, step)
        else:
            # decrease the approximation
            approx = fixed_nonnegative_diff(approx, step) # disgusting, will clean up later
    return approx


if __name__ == '__main__':
    sqrt_approx(100, 2).print()
    # to do: fix last digit, optimize, clean up the mess (refactor)