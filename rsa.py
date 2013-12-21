'''
Created on Nov 8, 2013

@author: Bishwa Hang Rai
@author: Thomas Kuehner
'''
import sys

#Checks if the Number is prime or not and returns boolean
def isPrime(num):
    for x in range(2,num):
        if(num % x == 0):
            return False
    return True;

#Solve the exponential function using Squaring method
#Algorithm from Wikipedia

def expoBySquaring(x,n):
    result = 1
    if (x == 0):
        return 0
    if (n == 0):
        return 1
    if (n == 1):
        return x
    if(n<0):
        x = 1.0/x
        n=-n
        expoBySquaring(x, n)

    while(n != 0):
        if (n % 2 == 0):
            n = n/2
            x = x * x
        else:
            result = result * x
            n = n-1
    return result;
    
#Compute all primes between 0 and max
#Input:
#max: maximum size of primes. Type: Integer
#Output:
#primes: ordered list of the primes between 1 and max

def computePrimes(max):
    primes = [x for x in range(2,max+1) if isPrime(x) == True]
    primes.sort()
    return primes
    


# Compute a public key
# Input:
# p, q: primes. Type: integer. Constraints: p, q < 300, p != q
# Output:
# (n, e): tupel of integers representing the public key
def computePubKey(p, q):
    assert (p < 300)
    assert (q < 300)
    assert (p != q)
    # Note: we do not do any primality tests here!
    # [YOUR TASK STARTS HERE]
    n= p * q;
    phi = computePhi(p, q) ;
    #Since the list of "e" to choose is already prime,
    #we need to only check if it is divisor of Prime
    for x in range(2,phi):
        if (gcd(x,phi) == 1):
            e=x
            break  #To take the smallest value, we break as soon we get our value from the sorted list
        
    # [YOUR TASK ENDS HERE]
    # n and e must be integers!
    return (n, e)
    
    

    
# e and phi(n) are input, both integers
# Compute a private key
# Input:
# e, phi(n): as in lecture. Type: integer.
# Output:
# d: private key. Type: integer
def computePrivKey(e, phi):
    # [YOUR TASK STARTS HERE]
    (x,y)=eea(e, phi)
    # [YOUR TASK ENDS HERE]
    # d is the private key, an integer
    return x


# gcd() uses eea()
# Input:
# a, b: numbers to work on. Type: integer
# Output:
# gcd: the gcd. Type: integer
def gcd(a, b):
    # [YOUR TASK STARTS HERE]
    #Using my knowledge of elementary math :)
    # fact stores all the exact divisor of both a,b
    fact=[1]
    low = a if a < b else b
    for i in range (2,low+1):
        #if the exact divisor is found store it, and change the dividend
        if (a % i == 0 ^ b % i == 0):
            fact = fact + [i]
            a, b = a / i, b / i
            low = a if a < b else b
            i = 2
    #result is product of all exact divisor
    gcd = reduce(lambda x, y: x*y, fact)

    # [YOUR TASK ENDS HERE]
    return gcd


# eea is the Extended Euclidean Algorithm
# Input:
# a, b: numbers to work on. Type: integer
# Output:
# (x, y): numbers for which ax + by = gcd(a,b) holds. Type: tupel of integers
def eea(a, b):
    # [YOUR TASK STARTS HERE]
    # a = e whose inverse is to be found
    # b = phi whose mod is used
    # gcd(a,b) is computed to check the breaking point of solution

    d=gcd(a, b)
    oldr,olds,oldt =a,1,0
    newr,news,newt =b,0,1
    while(True):
        q = oldr/newr
        tempr=oldr%newr
        temps=olds-q*news
        tempt=oldt-q*newt
        if(tempr == d):
            #Particular Solution has been found
            #Save the variable break the loop
            x,y=temps,tempt;
            break;
        oldr,olds,oldt=newr,news,newt
        newr,news,newt = tempr,temps,tempt
    #If x is negative make it positive
    x=(x*a)+b if x<0 else x
    # [YOUR TASK ENDS HERE]

    return (x, y)

# Compute phi(n) if input is a product of two primes
# Input:
# p, q: primes. Type: integer
# Output:
# o: phi(n). Type: integer
def computePhi(p, q):
    # [YOUR TASK STARTS HERE]
    # Axiomatic 
    o = (p-1) * (q-1)
    # [YOUR TASK ENDS HERE]
    return o



# Compute an encrypted message
# Input:
# m: the message. Type: integer. Constraint: m < n
# pubkey: public key. Type: tupel of integers (n, e)
# Output:
# ciphertext: encrypted message. Type: integer
def encrypt(m, pubkey):
    # [YOUR TASK STARTS HERE])
    
    me = expoBySquaring(m, pubkey[1])
    ciphertext= me % pubkey[0]
    
    # [YOUR TASK ENDS HERE]
    return ciphertext


# Decrypt an encrypted message
# Input:
# c: the ciphertext. Type: integer
# d: the private key. Type: integer
# n: the product of p and q. Type: integer
# Output:
# decryptedtext: the decrypted message. Type: integer
def decrypt(c, d, n):
    # [YOUR TASK STARTS HERE]
    
    cd = expoBySquaring(c, d)
    decryptedtext = cd % n;
    
    # [YOUR TASK ENDS HERE]
    return decryptedtext

# Use this if you want to test your program
# DO NOT CHANGE THE FORMAT OF COMMAND LINE CALL
# DO NOT CHANGE THE OUTPUT FORMAT
def main():
    # we read from stdin
    # first prime number
    p1 = int(sys.argv[1])
    # second prime number
    p2 = int(sys.argv[2])
    # message to encode, given as an integer m < n = p1 * p2
    m = int(sys.argv[3])
 
    # DO NOT CHANGE THE OUTPUT FORMAT
    (n, e) = computePubKey(p1, p2)
    print "Pubkey:" + str(n) + "," + str(e)
    phi = computePhi(p1, p2)
    print "Phi:" + str(phi)
    d = computePrivKey(e, phi)
    print "PrivKey:" + str(d)
    c = encrypt(m, (n, e))
    print "m:" + str(m) + "->" + str(c)
    print "c:" + str(c) + "->" + str(decrypt(c, d, n))

main()
