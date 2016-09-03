from random import randint, uniform


def insertion_sort(list):

    for j in range(1, len(list)):
        key = list[j]
        i = j
        while(i > 0) and list[i-1] > key:
            list[i] = list[i-1]
            i = i-1
        list[i] = key

    return list

def if_in_ascending(list):

    if len(list) <= 1:
        return True
    if list[-1] >= list[-2]:
        del list[-1]
        return if_in_ascending(list)
    else:
        return False

def if_in_ascending_helper(list):
    pass

A=[randint(0,9) for p in range(0,9)]

print insertion_sort(A), if_in_ascending(A)

B = [uniform(0.0,9.0) for f in range(0,20)]

print insertion_sort(B), if_in_ascending(B)

C, D, E = [4, 3], [], [500]

print if_in_ascending(C), if_in_ascending(D), if_in_ascending(E)