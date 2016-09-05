import sys
from random import randint, uniform

L_than = lambda A, B: A < B
G_than = lambda A, B: A > B
E_to = lambda A, B: A == B or A is B
G_E_to = lambda A, B: G_than(A, B) or E_to(A, B)
L_E_to = lambda A, B: L_than(A, B) or E_to(A, B)

my_round = lambda L, D: [round(i, D) for i in L ]
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # toy for interpretation

def insertion_sort(list, rule=G_E_to):
    ret = list
    for j in range(1, len(ret)):
        key = ret[j]
        i = j
        while(i > 0) and rule(ret[i-1], key):
            ret[i] = ret[i-1]
            i = i-1
        ret[i] = key
    return ret

def if_in_order(list, rule=G_E_to):
    ret = list
    if len(ret) <= 1:
        return True
    if rule(ret[-1], ret[-2]):
        del ret[-1]
        return if_in_order(ret, rule)
    return False

def test_ins_sort():

    ins=[randint(0,9) for x in range(0,9)]
    out = insertion_sort(ins, rule=L_E_to)

    print out, if_in_order(out, rule=L_E_to)

    ins = [uniform(0.0,9.0) for x in range(0,20)]
    out = insertion_sort(ins)
    print out, if_in_order(out)

def test_in_order():

    C, D, E = [3, 4], [], [500]

    print if_in_order(C), if_in_order(D), if_in_order(E)

    print ""

    F, G = [3, 4], [3, 4]
    print if_in_order(F, G_than), if_in_order(G, L_than)

    print ""

    print [ordinal(n) for n in F]

def test_rounding():

    ins = [uniform(0.0,9.0) for x in range(0,20)]
    out = my_round(insertion_sort(ins, rule=L_E_to), 4)
    temp = [i for i in out]

    print out, if_in_order(temp, rule=L_E_to)

if __name__ == '__main__':

    test_rounding()
    sys.exit(0)