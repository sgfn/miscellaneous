def pierwsze(n):
    count = 0
    for i in range(2, n//2+1):
        while n % i == 0:
            count += 1
            n //= i
        if count > 2:
            return False
    if count == 2:
        return True
    return False

def fun(tab1, tab2):
    for i in range(1, len(tab1)):
        for j in range(len(tab1) - i):
            suma = 0
            for indjeden in range(j, j + i):
                suma += tab1[indjeden]
            sumabackup = suma
            for k in range(len(tab1) - i):
                suma = sumabackup
                for ind2 in range(k, k - i):
                    suma += tab2[ind2]