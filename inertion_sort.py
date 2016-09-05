import sys, operator
from random import randint, uniform

my_round = lambda L, D: [round(i, D) for i in L ]
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # toy for interpretation
list_rand_int = lambda Lim, Len: [randint(0,Lim) for x in range(0,Len)]
list_rand_float = lambda Lim, Len: [uniform(0,Lim) for x in range(0,Len)]

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

def test_(input, operator=None):

    ins = insertion_sort(list(input), operator=operator)

    ins = my_round(list(ins), 4)

    print ins, if_in_order(list(ins), operator=operator), "\n"

if __name__ == '__main__':

    input = list_rand_int(10, 30)
    test_(input, operator=operator.ge)

    input = list_rand_float(10, 30)
    test_(input, operator=operator.ge)

    sys.exit(0)