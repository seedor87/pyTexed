import operator
from random import randint, uniform

def merge(left,right,compare):
    result=[]
    i,j=0,0
    while i<len(left) and j<len(right):
        if compare(right[j], left[i]):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    while (i<len(left)):
        result.append(left[i])
        i+=1
    while (j<len(right)):
        result.append(right[j])
        j+=1
    return result

def mergeSort(L,compare=operator.gt):
    if len(L)<2:
        return L[:]
    else:
        middle =int(len(L)/2)
        left=mergeSort(L[:middle], compare)
        right=mergeSort(L[middle:], compare)
        return merge(left,right,compare)

B = [randint(0.0,30.0) for f in range(0,20)]

res = mergeSort(B, compare=operator.gt)
print res