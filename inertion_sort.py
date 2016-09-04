from random import randint, uniform


def insertion_sort(list):
    ret = list
    for j in range(1, len(ret)):
        key = ret[j]
        i = j
        while(i > 0) and ret[i-1] > key:
            ret[i] = ret[i-1]
            i = i-1
        ret[i] = key
    return ret

L_than = lambda A, B: A < B
G_than = lambda A, B: A > B
E_to = lambda A, B: A == B or A is B
G_E_to = lambda A, B: G_than(A, B) or E_to(A, B)
L_E_to = lambda A, B: L_than(A, B) or E_to(A, B)

def if_in_order(list, rule=G_E_to):
    ret = list
    if len(ret) <= 1:
        return True
    if rule(ret[-1], ret[-2]):
        del ret[-1]
        return if_in_order(ret)
    return False

A=[randint(0,9) for p in range(0,9)]

print insertion_sort(A), if_in_order(A)

B = [uniform(0.0,9.0) for f in range(0,20)]

print insertion_sort(B), if_in_order(B)

C, D, E = [3, 4], [], [500]

print if_in_order(C), if_in_order(D), if_in_order(E)

print ""

F, G = [3, 4], [3, 4]
print if_in_order(F, G_than), if_in_order(G, L_than)

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]) # toy for interpretation

print ""

print [ordinal(n) for n in F]