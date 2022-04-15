# Dayton Dekam

import enum
from pyeda.inter import *

# Creates an x formula from a binary digit
def ToXFormula(binaryDigit):
    formula = ""

    for j, b in enumerate(binaryDigit): # second nodes
        if b == '0':
            formula += "~x" + str(j) + " & "
        elif b == '1':
            formula += "x" + str(j) + " & "
        else:
            print ("[Can't Translate Non-Binary]")
            quit() 

    return formula[:-3]

# Creates a y formula from a binary digit
def ToYFormula(binaryDigit):
    formula = ""

    for j, b in enumerate(binaryDigit): # second nodes
        if b == '0':
            formula += "~y" + str(j) + " & "
        elif b == '1':
            formula += "y" + str(j) + " & "
        else:
            print ("[Can't Translate Non-Binary]")
            quit() 

    return formula[:-3]

def TranslateToBinary(n):
    return bin(n)[2:].zfill(5) # string of 1s and 0s (5 characters)

# Translates a graph to a boolean formula
def GraphToBooleanFormula(graph):
    # must convert graph (int, int) into binary pairs
    R_list = [] # set of all possible edges (will be filled below)
    R_formulas = []
    booleanFormula = "" # will be the boolean formula to return

    # convert the graph's values to binary -> R_list
    for edge in graph:
        x = TranslateToBinary(edge[0]) # translates int to 5 digit binary
        y = TranslateToBinary(edge[1])
        R_list.append((x, y))

    # nested forloops to convert all binary pairs to boolean formula
    for binaryEdge in R_list:
        # formula for all x
        for i, b in enumerate(binaryEdge[0]): # first nodes
            if b == '0':
                booleanFormula += "~x" + str(i) + " & "
            elif b == '1':
                booleanFormula += "x" + str(i) + " & "
            else:
                print ("[Can't Translate Non-Binary in GraphToBooleanFormula()]")
                quit()

        for j, b in enumerate(binaryEdge[1]): # second nodes
            if b == '0':
                booleanFormula += "~y" + str(j) + " & "
            elif b == '1':
                booleanFormula += "y" + str(j) + " & "
            else:
                print ("[Can't Translate Non-Binary in GraphToBooleanFormula()]")
                quit()            
    
        booleanFormula = booleanFormula[:-3] # deletes the ampersand at the end
        R_formulas.append(booleanFormula)
        booleanFormula = "";

    return R_formulas

# Takes a formula and returns it's BDD
def FormulaToBDD(formulaList):
    formula = expr(formulaList.pop())
    bdd = expr2bdd(formula)

    while len(formulaList) > 0:
        nextFormula = expr(formulaList.pop())
        nextBDD = expr2bdd(nextFormula)
        bdd = bdd or nextBDD # appends BDDs with OR operator

    return bdd

# Performs a BDD Compose
def Compose(lhs, rhs):
    X = bddvars('x', 5) # creates an array of BDD vars
    Y = bddvars('y', 5)
    Z = bddvars('z', 5)
    
    R1 = lhs.compose({X[0]:Z[0], X[1]:Z[1], X[2]:Z[2], X[3]:Z[3], X[4]:Z[4]})
    R2 = rhs.compose({Z[0]:Y[0], Z[1]:Y[1], Z[2]:Y[2], Z[3]:Y[3], Z[4]:Y[4]})
    return (R1 and R2).smoothing(Z)

# Tests RR
def TestRR(RR, xx, yy):
    # Get binary of xx 
    x_bits = []
    x_binary = TranslateToBinary(xx)
    
    for i, b in enumerate(x_binary):
        if b == '0':
            x_bits.append(0)
        elif b == '1':
            x_bits.append(1)
        else:
            print("ERROR in TEST")
            quit()
            
    # Get binary of yy
    y_bits = []
    y_binary = TranslateToBinary(yy)
    
    for i, b in enumerate(y_binary):
        if b == '0':
            y_bits.append(0)
        elif b == '1':
            y_bits.append(1)
        else:
            print("ERROR in TEST")
            quit()

    # Create bddvars and test
    X = bddvars('x', 5)
    Y = bddvars('y', 5)
    
    result = RR.restrict({X[0]:x_bits[0], X[1]:x_bits[1], X[2]:x_bits[2], X[3]:x_bits[3], X[4]:x_bits[4], Y[0]:y_bits[0], Y[1]:y_bits[1], Y[2]:y_bits[2], Y[3]:y_bits[3], Y[4]:y_bits[4]})
    print(result)
    return

# Tests EVEN and PRIME BDDs
def TestOneValue(SET, n):
    X = bddvars('x', 5)
    bits = []
    n_binary = TranslateToBinary(n)
    
    for i, b in enumerate(n_binary):
        if b == '0':
            bits.append(0)
        elif b == '1':
            bits.append(1)
        else:
            print("ERROR in TEST")
            quit()
    
    result = SET.restrict({X[0]:bits[0], X[1]:bits[1], X[2]:bits[2], X[3]:bits[3], X[4]:bits[4]})
    print(result)
    return

# Computes transitive closure RR2star of R
def TransitiveClosure(R):
    val = None
    h = R
    
    while 1:
        h_prime = h
        h = h_prime or Compose(h_prime, R)

        if h.equivalent(h_prime):
            val = h
            break

    return val

# Tests Statement A for validity
def TestStatementA(RR2star, PRIME, EVEN):
    X = bddvars('x', 5)
    Y = bddvars('y', 5)
    
    return ~(~PRIME or ((EVEN and RR2star).smoothing(Y))).smoothing(X)

### Start of Code ####
if __name__ == "__main__":
    # create sets
    evenSet = []
    for n in range(0, 32):
        if n % 2 == 0:
            evenSet.append(n)

    primeSet = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    # Create the graph according to the following:
    # Let G be a graph over 32 nodes (namely, node 0, · · ·, node 31). For all 0 ≤ i, j ≤ 31, there is
    # an edge from node i to node j iff (i + 3)%32 = j%32 or (i + 8)%32 = j%32. 
    G_list = []
    for i in range(0, 32):
        for j in range(0, 32):
            if ((i + 3) % 32 == j % 32) or ((i + 8) % 32 == j % 32):
                G_list.append((i, j))

    # Translate G's edges (R) to boolean formulas
    G_formulas = GraphToBooleanFormula(G_list)
    
    ### Translate primeSet into a boolean expression
    binaryPrimeSet = []
    primeFormulas = []
    primeBooleanFormula = ""

    for n in primeSet: # first convert to binary
        binaryPrimeSet.append(TranslateToBinary(n))
        
    # walk through each prime node's binary digits and translate to boolean formula
    for primeNode in binaryPrimeSet:
        primeBooleanFormula = ToXFormula(primeNode)
        primeFormulas.append(primeBooleanFormula)
        primeBooleanFormula = "";
    
    ### Translate evenSet into a boolean expression
    binaryEvenSet = []
    evenFormulas = []
    evenBooleanFormula = ""
    
    for n in evenSet: # convert to binary
        binaryEvenSet.append(TranslateToBinary(n))
        
    # walk through each even node's binary digits and translate to boolean formula
    for evenNode in binaryEvenSet:
        evenBooleanFormula = ToYFormula(evenNode)
        evenFormulas.append(evenBooleanFormula)
        evenBooleanFormula = ""

    ### Convert Boolean Formulas to BDDs (G, evens, primes)
    # use the expr2bdd function to convert arbitrary expressions to BDDs
    RR = FormulaToBDD(G_formulas)
    PRIME = FormulaToBDD(primeFormulas)
    EVEN = FormulaToBDD(evenFormulas)
    
    ### Run Tests
    print("[TESTS FOR RR, PRIME, AND EVEN]")
    TestRR(RR, 27, 3)       # TRUE
    TestRR(RR, 16, 20)      # FALSE
    TestOneValue(EVEN, 14)  # TRUE
    TestOneValue(EVEN, 13)  # FALSE
    TestOneValue(PRIME, 7)  # TRUE
    TestOneValue(PRIME, 2)  # FALSE
    
    ### Compute BDD RR2 for the set R ◦ R, from BDD RR. Herein, RR2 encodes
    ### the set of node pairs such that one can reach the other in two steps.
    RR2 = Compose(RR, RR)
    
    print("\n[TESTS FOR RR2]")
    TestRR(RR2, 27, 6)      # TRUE
    TestRR(RR2, 27, 9)      # FALSE
    
    ###Compute the transitive closure RR2star of RR2. Herein, RR2star encodes 
    # the set of all node pairs such that one can reach the other in a positive even number of steps.
    RR2star = TransitiveClosure(RR2)
    
    ### Statement A: ∀u. (PRIME(u) → ∃v. (EVEN(v)∧RR2star(u,v))).
    print("\n[TESTING STATEMENT A]")
    statementA = TestStatementA(RR2star, PRIME, EVEN)
    
    if (statementA):
        print("Statement A IS TRUE:   for each node u in [prime], there is a node v in [even] such that u can reach v in a positive even number of steps.")
        
    else:
        print("Statement A IS FALSE")
