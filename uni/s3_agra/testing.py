import os
import multiprocessing
from time import perf_counter

import dimacs


class clr:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cs(s, c):
    return f'{c}{s}{clr.ENDC}'


def load_and_test_graph(name, fun, directed=False, time_limit=5, cnf=False):
    def fun_wrapper(fun, q, *args, **kwargs):
        q.put(fun(*args, **kwargs))


    if directed:
        V, edge_list = dimacs.loadDirectedWeightedGraph(name)
    elif cnf:
        V, edge_list = dimacs.loadCNFFormula(name)
    else:
        V, edge_list = dimacs.loadWeightedGraph(name)
    sol = dimacs.readSolution(name)

    t_s = perf_counter()
    try:
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=fun_wrapper, args=(fun, q, V, edge_list), name=f'testing_{fun.__name__}')
        p.start()
        p.join(time_limit)
        timeout = p.is_alive()
        if timeout:
            p.terminate()
            p.join()
            failed = False
        else:
            res = q.get()
            failed = not int(sol) == int(res)

    except RecursionError:
        res = 'RecursionError'
        failed = True
    t_e = perf_counter()

    print(cs('[FAIL]',clr.FAIL) if failed else (cs('[TIME]',clr.WARNING) if timeout else cs('[PASS]',clr.OKGREEN)), fun.__name__, '%6.3f s' % (t_e-t_s), name, sep='    ')
    if failed:
        print(f'\texpected {sol}, got {res}')

    return not failed and not timeout


def test_from_dir(path, *funs, more_paths=None, directed=False, time_limit=5, cnf=False):
    results = [None for _ in funs]
    times = [None for _ in funs]
    paths = [path]
    if more_paths is not None:
        paths.extend(more_paths)
    files = []
    for p in paths:
        files.extend((os.path.join(p, f) for f in os.listdir(p)))

    t_s = perf_counter()
    for i, fun in enumerate(funs):
        passed = 0
        t_s_fun = perf_counter()
        for path_to_test in files:
            if load_and_test_graph(path_to_test, fun, directed, time_limit, cnf):
                passed += 1
        t_e_fun = perf_counter()
        results[i] = passed
        times[i] = t_e_fun - t_s_fun
    t_e = perf_counter()

    print()
    for i, fun in enumerate(funs):
        print(f'{fun.__name__}: {results[i]}/{len(files)} tests passed ({"%.3f s" % times[i]})')

    print(cs(f'TOTAL: {sum(results)}/{len(files)*len(funs)} tests passed ({"%.3f s" % (t_e-t_s)})\n', clr.BOLD))
