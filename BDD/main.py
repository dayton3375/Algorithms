import enum
from pyeda.inter import *

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

def FormulaToBDD(formulaList):
    formula = expr(formulaList.pop())
    bdd = expr2bdd(formula)

    while len(formulaList) > 0:
        nextFormula = expr(formulaList.pop())
        nextBDD = expr2bdd(nextFormula)
        bdd = bdd or nextBDD # appends BDDs with OR operator

    return bdd

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
        for i, b in enumerate(primeNode):
            if b == '0':
                primeBooleanFormula += "~x" + str(i) + " & "
            elif b == '1':
                primeBooleanFormula += "x" + str(i) + " & "
            else:
                print("[Can't do non-binary from prime set]")
                quit()
        primeBooleanFormula = primeBooleanFormula[:-3] # deletes the ampersand at the end
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
        for j, b in enumerate(evenNode):
            if b == '0':
                evenBooleanFormula += "~y" + str(j) + " & "
            elif b == '1':
                evenBooleanFormula += "y" + str(j) + " & "
            else:
                print("[Can't do non-binary from even set]")
                quit()               
        evenBooleanFormula = evenBooleanFormula[:-3] # deletes the ampersand at the end
        evenFormulas.append(evenBooleanFormula)
        evenBooleanFormula = ""

    ### Convert Boolean Formulas to BDDs (G, evens, primes)
    # use the expr2bdd function to convert arbitrary expressions to BDDs
    RR = FormulaToBDD(G_formulas)
    PRIME = FormulaToBDD(primeFormulas)
    EVEN = FormulaToBDD(evenFormulas)
    
    ### Compute BDD RR2 for the set R ◦ R, from BDD RR. Herein, RR2 encodes
    ### the set of node pairs such that one can reach the other in two steps.
    