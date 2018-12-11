# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice_util(text,i,j):
    assert(i<=j)

    if longest_subpalindrome_slice_util.table[i][j] != (-1,-1):
        return longest_subpalindrome_slice_util.table[i][j]
    
    assert(i<j)

    if i+1 == j:
        if text[i]!=text[j]:
            (x,y) = (i,i)
        else:
            (x,y) = (i,j)
    else:
        (x,y) = (-1,-1)
        if text[i] == text[j]:
            (x,y) = longest_subpalindrome_slice_util(text,i+1,j-1)
            if i==x-1 and j==y+1:
                (x,y) = (i,j)
        (p,q) = longest_subpalindrome_slice_util(text,i+1,j)
        (m,n) = longest_subpalindrome_slice_util(text,i,j-1)
        (d,e) = (p,q) if ((q-p)>=(n-m)) else (m,n)
        (x,y) = (x,y) if (x,y)!=(-1,-1) and ((y-x)>=(e-d)) else (d,e)
    
    longest_subpalindrome_slice_util.table[i][j] = (x,y) 
    return  (x,y)

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    n = len(text)
    if n==0: return (0,0)
    table = [ [(-1,-1) if i!=j else (i,j) for i in range(0,n)] for j in range(0,n) ]
    longest_subpalindrome_slice_util.table = table
    (x,y) = longest_subpalindrome_slice_util(text.lower(),0,n-1)
    return (x,y+1)

def test():
    L = longest_subpalindrome_slice
    assert(L('racecar') == (0, 7))
    assert(L('Racecar') == (0, 7))
    assert(L('RacecarX') == (0, 7))
    assert(L('Race carr') == (7, 9))
    assert(L('') == (0, 0))
    assert(L('something rac e car going') == (8,21))
    assert(L('xxxxx') == (0, 5))
    assert(L('Mad am I ma dam.') == (0, 15))
    return 'tests pass'

print(test())