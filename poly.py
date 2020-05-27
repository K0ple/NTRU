# Polynomial Module 
from operator import add
from operator import neg
from operator import mod
from fractions import Fraction as frac
from numpy.polynomial import polynomial as P

# Resize Adds Leading Zeros to the polynomial vectors

#Helper Functions 
# Extended Euclidean Algo for Integers

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u * q, y-v * q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcdVal = b
    return gcdVal, x, y


#Modular inverse
#An application of extended GCD algorithm to finding modular inverses:
def modinv(a, m):
    gcdVal, x, y = egcd(a, m)
    if gcdVal != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

#Modulus Function which handles Fractions aswell
def fracMod(f,m):
	[tmp,t1,t2]=egcd(f.denominator,m)
	if tmp!=1:
		print("ERROR GCD of denominator and m is not 1")
		return 0
	else:
		out=modinv(f.denominator,m)*f.numerator % m
		return out


def resize(c1,c2):
	if(len(c1)>len(c2)):
		c2=c2+[0]*(len(c1)-len(c2))
	if(len(c1)<len(c2)):
		c1=c1+[0]*(len(c2)-len(c1))
	return [c1,c2]

# Removes Leading Zeros
def trim(seq):
	if len(seq) == 0:
		return seq
	else:
		for i in range(len(seq) - 1, -1, -1):
			if seq[i] != 0:
				break
		return seq[0:i+1]

# Subtracts two Polnomials
def subPoly(c1,c2):
	[c1,c2]=resize(c1,c2)	
	c2=list(map(neg,c2))
	out=list(map(add, c1, c2))
	return trim(out)

# Adds two Polynomials
def addPoly(c1,c2):
	[c1,c2]=resize(c1,c2)
	out=list(map(add, c1, c2))
	return trim(out)

# Multiply two Polynomials 
def multPoly(c1,c2):
        order=(len(c1)-1+len(c2)-1)
        out=[0]*(order+1)
        for i in range(0,len(c1)):
                for j in range(0,len(c2)):
                        out[j+i]=out[j+i]+c1[i]*c2[j]
        return trim(out)

#Divides two polynomials
def divPoly(N,D):
	N, D = list(map(frac,trim(N))), list(map(frac,trim(D)))
	degN, degD = len(N)-1, len(D)-1
	if(degN>=degD):
		q=[0]*(degN-degD+1)
		while(degN>=degD and N!=[0]):
			d=list(D)
			[d.insert(0,frac(0,1)) for i in range(degN-degD)]
			q[degN-degD]=N[degN]/d[len(d)-1]
			d=list(map(lambda x: x*q[degN-degD],d))
			N=subPoly(N,d)
			degN=len(N)-1
		r=N	
	else:
		q=[0]
		r=N
	return [trim(q),trim(r)]

# Polynomial Coefficients mod k
def modPoly(c,k):
	if(k==0):
		print("Error in modPoly(c,k). Integer k must be non-zero")
	else:
		return list(map(lambda x: fracMod(x,k),c))

# Centerlift of Polynomial with respect to q
def cenPoly(c,q):
	u=float(q)/float(2)
	l=-u
	c=modPoly(c,q)
	c=list(map(lambda x: mod(x,-q) if x>u else x,c))
	c=list(map(lambda x: mod(x,q) if x<=l else x,c))
	return c

# Extended Euclidean Algorithm
def extEuclidPoly(a,b):
    switch = False
    a=trim(a)
    b=trim(b)
    if len(a)>=len(b):
        a1, b1 = a, b
    else:
        a1, b1 = b, a
        switch = True
    Q,R=[],[]
    while b1 != [0]:
        [q,r]=divPoly(a1,b1)
        Q.append(q)
        R.append(r)
        a1=b1
        b1=r
    S=[0]*(len(Q)+2)
    T=[0]*(len(Q)+2)
    S[0],S[1],T[0],T[1] = [1],[0],[0],[1]
    for x in range(2, len(S)):
        S[x]=subPoly(S[x-2],multPoly(Q[x-2],S[x-1]))
        T[x]=subPoly(T[x-2],multPoly(Q[x-2],T[x-1]))

    gcdVal=R[-2]
    s_out=S[-2]
    t_out=T[-2]
    ### ADDITIONAL STEPS TO SCALE GCD SUCH THAT LEADING TERM AS COEF OF 1:
    scaleFactor=gcdVal[len(gcdVal)-1]
    gcdVal=list(map(lambda x:x/scaleFactor,gcdVal))
    s_out=list(map(lambda x:x/scaleFactor,s_out))
    t_out=list(map(lambda x:x/scaleFactor,t_out))
    if switch:
        return [gcdVal,t_out,s_out]
    else:
        return [gcdVal,s_out,t_out]
	


def isTernary(f,alpha,beta):
	ones=0
	negones=0
	for i in range(0,len(f)):
		if(f[i]==1):
			ones=ones+1
		if(f[i]==-1):
			negones=negones+1
	if (negones+ones)<=len(f) and alpha==ones and beta==negones :
		return True
	else:
		return False
