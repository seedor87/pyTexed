import sys, operator
from random import randint, uniform

my_round = lambda L, D: [round(i, D) for i in L ]
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # toy for interpretation

def insertion_sort(list, operator=operator.ge):
    ret = list
    for j in range(1, len(ret)):
        key = ret[j]
        i = j
        while(i > 0) and operator(ret[i-1], key):
            ret[i] = ret[i-1]
            i = i-1
        ret[i] = key
    return ret

def if_in_order(list, operator=operator.ge):
    ret = list
    if len(ret) <= 1:
        return True
    if operator(ret[-1], ret[-2]):
        del ret[-1]
        return if_in_order(ret, operator)
    return False

def test_ins_sort():

    ins=[randint(0,9) for x in range(0,9)]
    out = insertion_sort(ins, operator=operator.le)

    print out, if_in_order(out, operator=operator.le)

    ins = [uniform(0.0,9.0) for x in range(0,20)]
    out = insertion_sort(ins)
    print out, if_in_order(out)

def test_in_order():

    C, D, E = [3, 4], [], [500]

    print if_in_order(C), if_in_order(D), if_in_order(E)

    print ""

    F, G = [3, 4], [3, 4]
    print if_in_order(F, operator.ge), if_in_order(G, operator.le)

    print ""

    print [ordinal(n) for n in F]

def test_rounding():

    ins = [uniform(0.0,9.0) for x in range(0,20)]
    out = my_round(insertion_sort(ins, operator=operator.ge), 4)
    temp = [i for i in out]

    print out, if_in_order(temp, operator=operator.ge)

if __name__ == '__main__':

    test_rounding()
    sys.exit(0)