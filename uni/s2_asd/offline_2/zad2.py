# Jakub Pisarek
# 
# Rozwiązanie bazuje na algorytmie sortowania szybkiego (quicksort), zoptymali-
# zowanego dla mniejszych tablic za pomocą algorytmu sortowania przez wstawianie
# (insertion sort). Po posortowaniu listy przedziałów według pierwszej współ-
# rzędnej (początku przedziału), dla każdego przedziału wykonywane jest spraw-
# dzenie z każdym innym przedziałem, którego początek przypada wewnątrz wyjścio-
# wego przedziału. Jeżeli wykryte zostanie, że dany przedział w całości zawiera
# się w innym, to ten przedział później zostanie pominięty, bo nie może być
# przedziałem o najwyższym poziomie. Pesymistyczna złożoność obliczeniowa wynosi
# O(n^2) zarówno ze względu na algorytm quicksort (choć w praktyce szanse wystą-
# pienia takiego przypadku są nikłe z racji na wybór pivota jako mediany trzech 
# różnych elementów z tablicy), jak i na końcowe porównania (najgorszy przypadek
# to przedziały zachodzące na siebie, niezawierające się). W praktyce jednak
# średnią złożoność obliczeniową szacuję na O(n log n), gdyż po pierwsze, taka
# jest średnia złożoność sortowania, zaś po drugie, choć może ciężko mówić o
# średnim przypadku, to samo sprawdzanie warunku zadania wymaga gdzieś pomiędzy 
# cn a cn^2 operacji i w przeważającej większości przypadków nie wpływa znacząco
# na wydłużenie czasu działania programu.
# Złożoność pamięciowa programu wynosi O(log n + n) = O(n).
# 
# Komentarze autora (tj. moje) wewnątrz kodu zostały wykonane w jęz. angielskim.

from zad2testy import runtests


def depth(L):
    STACK_SIZE   = 24   # Sorting algorithm function call stack size
    QS_THRESHOLD = 20   # Threshold for using the quicksort algorithm

    n = len(L)
    
    # Sort the list using a mixed algorithm (quicksort + insertion sort)
    # Create and initialise a function call stack
    qs_stack    = [(None, None) for _ in range(STACK_SIZE)]
    qs_stack[0] = (0, n-1)
    qs_top      = 1

    while qs_top > 0:
        qs_top -= 1
        left, right = qs_stack[qs_top]

        # Use insertion sort for small subarrays
        if right-left < QS_THRESHOLD:
            i = left + 1
            while i <= right:
                x, y = L[i]
                j = i - 1
                while j >= 0 and L[j][0] > x:
                    L[j+1] = L[j]
                    j -= 1
                L[j+1] = [x, y]
                i += 1

        # Use quicksort for larger subarrays
        else:
            # Choose a pivot point (median of first, middle and last elements)
            el_1 = L[left][0]
            el_2 = L[(left+right)>>1][0]
            el_3 = L[right][0]
            if el_1 < el_2:
                if   el_2 < el_3:   pivot = el_2
                elif el_1 < el_3:   pivot = el_3
                else:               pivot = el_1
            else:
                if   el_1 < el_3:   pivot = el_1
                elif el_2 < el_3:   pivot = el_3
                else:               pivot = el_2

            # Perform the main body of quicksort
            i = left
            j = right
            while i <= j:
                while L[i][0] < pivot:
                    i += 1
                while L[j][0] > pivot:
                    j -= 1
                if i <= j:
                    L[i], L[j] = L[j], L[i]
                    i += 1
                    j -= 1

            # Add appropriate ranges to the call stack
            if left < j:
                if i < right:
                    # If both ranges are to be sorted, make sure to handle
                    # the shorter one first, as that minimises the risk of a
                    # stack overflow
                    if j - left < right - i:
                        qs_stack[qs_top]   = (i, right)
                        qs_stack[qs_top+1] = (left, j)
                    else:
                        qs_stack[qs_top]   = (left, j)
                        qs_stack[qs_top+1] = (i, right)
                    qs_top += 2
                else:    
                    qs_stack[qs_top] = (left, j)
                    qs_top += 1
            elif i < right:
                qs_stack[qs_top] = (i, right)
                qs_top += 1
    
    # Calculate the answer
    # Create a helper array with flags telling if range can be of maximum depth
    check_range = [True for _ in range(n)]

    i = 0
    ans = 0

    # Create a helper variable storing the index of the first range that has the
    # same starting point as current range
    r_begin_first = 0

    while i < n:
        r_begin, r_end = L[i]
        if r_begin > L[r_begin_first][0]:   r_begin_first = i

        if check_range[i]:
            counter = -1    # Subtract 1 as each range contains itself
            j = r_begin_first
            while j < n and L[j][0] <= r_end:
                if L[j][1] <= r_end:    # Range is contained by another
                    counter += 1
                    check_range[j] = False
                j += 1
            if counter > ans:   ans = counter
        
        i += 1

    return ans


runtests( depth ) 
