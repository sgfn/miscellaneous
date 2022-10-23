"""
Jakub Pisarek

Problem przedstawiony w zadaniu jest analogiczny do problemu znajdowania cyklu
Hamiltona w grafie nieskierowanym, który to problem jest NP-zupełny. Oznacza to,
że działająca w czasie wielomianowym solucja do niego (dla przypadku ogólnego)
nie istnieje i istnieć nie ma prawa, czego dowiedli ludzie znacznie mądrzejsi
ode mnie.

Skoro zostało powiedziane, co powiedziane zostać winno, przejdźmy do omówienia
algorytmu. Jest to zwykły algorytm brute-force, sprawdzający wszystkie możliwo-
ści (miasto i brama startowa są wybierane losowo, co w żaden sposób nie wpływa
na poprawność znajdowanego rozwiązania) - stąd pewność o jego poprawności.
Został on minimalnie usprawniony za cenę użycia O(n^2) dodatkowej pamięci -
w tablicy `wgsbn` przechowujemy informację, do której bramy musimy się udać nas-
tępnie, dzięki czemu nie musimy za każdym razem tej informacji szukać w czasie
liniowym.

Złożoność obliczeniowa rozwiązania wynosi O(n!).
"""

from zad7testy import runtests

from random import randint

def droga( G ):
    N = len(G)
    START_NODE = randint(0, N-1)
    START_GATE = randint(0, 1)
    
    # Which gate should be next? Find and store the answer beforehand - O(n^2)
    wgsbn = [[9001 for _ in G] for _ in G]
    for city_to, (gate_n, gate_s) in enumerate(G):
        for city_from in gate_n:        wgsbn[city_to][city_from] = 1
        for city_from in gate_s:        wgsbn[city_to][city_from] = 0

    visited = [False for _ in G]
    history = []
    
    def recursive(curr_no, use_gate, depth):
        if depth == N:          return curr_no == START_NODE and use_gate == START_GATE
        if visited[curr_no]:    return False

        history.append(curr_no)
        visited[curr_no] = True

        for next_no in G[curr_no][use_gate]:
            if recursive(next_no, wgsbn[next_no][curr_no], depth+1):
                return True
                
        visited[curr_no] = False
        history.pop()
        return False

    recursive(START_NODE, START_GATE, 0)
    return history if history else None
    

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( droga, all_tests = True )
