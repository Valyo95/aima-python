import sys  
sys.path.append("aima-python")
import csp
import itertools
import time
from utils import count

from ast import  literal_eval


def cage_ok(A,a):

    cage = kenken.cages[A]
    if A in cage.points:
        #print("Assignments", kenken.assignment)
        #print ("A is ", A, "a is ", a)
        #print(cage)
        if len(cage.points) == 1:
            if int(a) != cage.result:
                return False
            else:
                return True

        if cage.operator == "add":
            sum = 0
            assigned = 0
            for point in cage.points:
                if point in kenken.assignment.keys():
                    if point == A:
                        sum+= int(a)
                        continue
                    sum+= int(kenken.assignment[point])
                    assigned+=1
                else:

                    if point == A:
                        sum+= int(a)
            if assigned == len(cage.points)-1:
                return sum == int(cage.result)
            if sum <= int(cage.result):
                return True
            else:
                return False
        if cage.operator == "mult":
            mul = 1
            assigned = 0
            for point in cage.points:
                if point in kenken.assignment.keys():
                    if point == A:
                        mul*= int(a)
                        continue

                    mul*= int (kenken.assignment[point])
                    assigned+= 1
                else:
                    if point == A:
                        mul*= int(a)
            if assigned == len(cage.points) -1:
                return mul == int(cage.result)
            if mul <= int(cage.result):
                return True
            else:
                return False
        if cage.operator == "sub":
            if cage.points[0] == A:
                if cage.points[1] in kenken.assignment.keys():
                    b = int(kenken.assignment[cage.points[1]])
                    return abs(a-b) == cage.result
                else:
                    return True
            else:
                if cage.points[0] in kenken.assignment.keys():
                    b = int(kenken.assignment[cage.points[0]])
                    return abs(a - b) == cage.result
                else:
                    return True

        if cage.operator == "div":
            if cage.points[0] == A:
                if cage.points[1] in kenken.assignment.keys():
                    b = int(kenken.assignment[cage.points[1]])
                    if a > b:
                        return a/b == cage.result
                    else:
                        return b/a == cage.result
                else:
                    return True
            else:
                if cage.points[0] in kenken.assignment.keys():
                    b = int(kenken.assignment[cage.points[0]])
                    if a > b:
                        return a/b == cage.result
                    else:
                        return b/a == cage.result
                else:
                    return True


def my_constrait(A, a, B, b):
    kenken.constraint+= 1
    return int(a)!=int(b) and cage_ok(A,int(a))


class Cage:
    def __init__(self):
        self.points = list()
        self.operator = None
        self.result = None

    def __repr__(self):
        print("Points: ", self.points)
        print("Operator: ", self.operator)
        print("Result: ", self.result)
        return ""

def coordinates_to_point(cor, size):
    return cor[0]*size + cor[1]

def split_line(s, delim):
    for ele in s.split(delim):
        try:
            yield literal_eval(ele)
        except ValueError:
            yield ele

def get_input(fileName, dict_cages):
    lines = [line.rstrip('\n') for line in open(fileName)]

    size = int(lines.pop(0))
    numOfCages = lines.__len__()

    cages = [Cage() for i in range(numOfCages)]

    for i,line in enumerate(lines):
        line = (list(split_line(line, ' ')))
        cages[i].operator = line[1]
        cages[i].result = int(line[2])
        for point in line[0]:
            p = coordinates_to_point(point,size)
            cages[i].points.append(p)
            dict_cages[p] = cages[i]

    return dict_cages,size





class Kenken(csp.CSP):


    def __init__(self, cages,size, neighbors, var):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        self.size = size
        self.cages = cages
        self.neighbors = neighbors
        self.assignment = {}
        self.variables = var
        self.nassigns = 0
        self.constraint = 0
        #print (size)
        domain = '123456789'
        domain = domain[:-(9-size)]
        #print (domain)
        domains = {}
        for i in self.variables:
            domains[i] = domain

        csp.CSP.__init__(self, self.variables, domains, self.neighbors, my_constrait)


    def assign(self, var, val, assignment):
        "Add {var: val} to assignment; Discard the old value if any."
        assignment[var] = val
        self.assignment[var] = int(val)
        self.nassigns += 1
        #print (assignment)

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            del self.assignment[var]

    def display(self):
        i = 0
        space = "------"
        for assign in self.assignment:
            if i%self.size == 0:
                print()
                for b in range(size):
                    print(space,end="")
                print("-\n|  ", end="")
            print(self.assignment[assign], end="  |  ")
            i+=1
        print()
        for b in range(size):
            print(space, end="")
        print("-")

    #______________________________________________________________________________



#--------Program execution--------#
#-------------------------------------------#
#-------------------------------------------#
#-------------------------------------------#

inn = "tests/in"
for i in range(3,8):
    avTime = 0
    avAssigns = 0
    avConstraints = 0
    board = str(i) + "x" + str(i)
    for j in range(1,3):
        input = inn+board+"_"+str(j)+".txt"
        print("\n\n")
        print("Running Kenken for:", input)


        dict_cages = {}
        dict_cages,size = get_input(input, dict_cages)


        _R = list(range(size))
        _CELL = itertools.count().__next__

        _ROWS = [[_CELL() for x in _R] for y in _R]
        _COLS = list(zip(*_ROWS))

        _NEIGHBORS = {v: set() for v in csp.flatten(_ROWS)}
        for unit in map(set, _ROWS + _COLS):
            for v in unit:
                _NEIGHBORS[v].update(unit - set([v]))

        var = []

        [var.append(i) for i in range(size ** 2)]


        neighbors = _NEIGHBORS

        kenken = Kenken(dict_cages, size, neighbors,var)
        #print (kenken.var)
        #print (kenken.domains)
        #print (kenken.neighbors)
        #print(kenken.cages)

        start = time.time()

        #--------------Algorithms---------------#
        #--------Choose whoever you want--------#
        #---------------------------------------#

        csp.backtracking_search(kenken)
        #csp.backtracking_search(kenken, select_unassigned_variable=csp.mrv)
        #csp.backtracking_search(kenken, inference=csp.forward_checking)
        #csp.backtracking_search(kenken, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
        #csp.backtracking_search(kenken, inference=csp.mac)
        #csp.min_conflicts(kenken)

        #---------------------------------------#

        end = time.time()

        kenken.display()
        print("Time elapsed: %.5f" % (end - start), "seconds")
        print("Assigns:", kenken.nassigns)
        print("Times that entered in my_constraints:", kenken.constraint)


        # --------------Statistics---------------#
        # ---------------------------------------#
        avTime += end - start
        avAssigns += kenken.nassigns
        avConstraints += kenken.constraint
        #---------------------------------------#

    print()
    print("Statistics for board size:", board)
    print("Average Time: %.5f" % (avTime/2), "seconds")
    print("Average Assignments:", avAssigns/2)
    print("Average calls of my_constraints:", avConstraints/2)



#If you wanna choose a specific test then comment the above one and uncomment the below as you add your own input 


"""
input = "in.txt"
print("\n\n")
print("Running Kenken for:", input)


dict_cages = {}
dict_cages,size = get_input(input, dict_cages)


_R = list(range(size))
_CELL = itertools.count().__next__

_ROWS = [[_CELL() for x in _R] for y in _R]
_COLS = list(zip(*_ROWS))

_NEIGHBORS = {v: set() for v in csp.flatten(_ROWS)}
for unit in map(set, _ROWS + _COLS):
    for v in unit:
        _NEIGHBORS[v].update(unit - set([v]))

var = []

[var.append(i) for i in range(size ** 2)]


neighbors = _NEIGHBORS

kenken = Kenken(dict_cages, size, neighbors,var)
#print (kenken.var)
#print (kenken.domains)
#print (kenken.neighbors)
#print(kenken.cages)

#--------------Algorithms---------------#
#---------------------------------------#
start = time.time()
#csp.backtracking_search(kenken)
#csp.backtracking_search(kenken, select_unassigned_variable=csp.mrv)
#csp.backtracking_search(kenken, inference=csp.forward_checking)
#csp.backtracking_search(kenken, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
csp.backtracking_search(kenken, inference=csp.mac)
#csp.min_conflicts(kenken)
end = time.time()
#---------------------------------------#

kenken.display()
print("Time elapsed: %.5f" % (end - start), "seconds")
print("Assigns:", kenken.nassigns)
print("Times that entered in my_constraints:", kenken.constraint)


"""
