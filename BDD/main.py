from pyeda.inter import *

def TranslateToBinary(n):
    return bin(n)[2:].zfill(5)

# Translates a graph to a boolean formula
def GraphToBooleanFormula(graph):

# must convert graph (int, int) into binary pairs
    binaryList = []
    booleanFormula = "" # will be the boolean formula to return

    # convert the graph's values to binary -> binaryList
    for edge in graph:
        x = TranslateToBinary(edge[0]) # translates int to 5 digit binary
        y = TranslateToBinary(edge[1])
        binaryList.append((x, y))

    # nested forloops to convert all binary pairs to boolean formula
    for binaryEdge in binaryList:
        # formula for all x
        for i, b in enumerate(binaryEdge[0]): # first nodes
            if (b == '0'):
                booleanFormula += "~x" + str(i) + " & "
            elif (b == '1'):
                booleanFormula += "x" + str(i) + " & "
            else:
                print ("[Can't Translate Non-Binary in GraphToBooleanFormula()]")
                return None;
        for j, b in enumerate(binaryEdge[1]): # second nodes
            if (b == '0'):
                booleanFormula += "~y" + str(j) + " & "
            elif (b == '1'):
                booleanFormula += "y" + str(j) + " & "
            else:
                print ("[Can't Translate Non-Binary in GraphToBooleanFormula()]")
                return None;            
    
    return booleanFormula    

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

    # Translate G (graph) to a boolean formula
    G_binary_formula = GraphToBooleanFormula(G_list)

    # use the expr2bdd function to convert arbitrary expressions to BDDs
