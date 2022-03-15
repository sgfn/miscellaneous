def waga(n):
    pass

def zad2(W, suma, i=0, s=[], flag=False):
    if sum(s) > suma:
        return False

    if sum(s) == suma:
        if flag == False:
            a = W.copy()
            for el in s:
                a.remove(el)
            return zad2(a, suma, s=[], flag=True)
        else:
            return True
    if i>=len(W):
        return False
    b = W[i]
    x = s.copy()
    x.append(b)
    return zad2(W, suma, i+1, s, flag) or zad2(W, suma, i+1, x, flag)
    

def rozw(T):
    W = [waga(val) for val in T]
    W = [1, 2, 3]
    suma = sum(W)
    if suma % 3 != 0:
        return False
    suma //= 3
    return zad2(W, suma)

if __name__ == '__main__':
    T = []
    print(rozw(T))
