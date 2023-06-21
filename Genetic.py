import copy
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse

class node:
    def __init__(self,value,parent = None):
        self.value = value
        self.parent = parent
        self.leftChild = None
        self.rightChild = None   #if our value = sin or cos => we just have left child
        self.MSE = None

    def __str__(self):
        return 'value: ' + str(self.value) +'\tparent:' +str(self.parent)
        


def printTree(node):
    if node.leftChild== None and node.rightChild == None:
        return node.value 

    else :
        LeftSum = printTree(node.leftChild) 
        if ['+','-','*','/','**'].__contains__(node.value):
            RightSum = printTree(node.rightChild)
            return '(' + str(LeftSum)+str(node.value)+str(RightSum)+')'
        else :
            return str(node.value)+'(' + str(LeftSum) + ')'
        
def all_nodes(T):
    mylist = []
    mylist.append(T)
    if T.leftChild != None:
        mylist.extend(all_nodes(T.leftChild))
    if T.rightChild != None:
        mylist.extend(all_nodes(T.rightChild))
    return mylist

def Jahesh(tree):
    node_list = all_nodes(tree)
    chosen_node = random.choice(node_list)

    operators = ['+','-','*','/','**','math.sin','math.cos']
    numbers = [1,2,3,4,5,6,7,8,9,10,'x']
    if operators.__contains__(chosen_node.value):
        if chosen_node.value=='math.sin' or chosen_node.value=='math.cos':
            chosen_node.value = random.choice(['math.sin','math.cos'])
        else:
            chosen_node.value = random.choice(['+','-','*','/','**'])
    else :
        chosen_node.value = random.choice(numbers)
    return tree

def combineTrees(T1,T2):
    NewTree1 = copy.deepcopy(T1)
    NewTree2 = copy.deepcopy(T2)

    T1_nodes_list = all_nodes(NewTree1)
    T2_nodes_list = all_nodes(NewTree2)

    selected_t1_node = random.choice(T1_nodes_list)
    selected_t2_node = random.choice(T2_nodes_list)
    
    selected_t1_node.value , selected_t2_node.value = selected_t2_node.value , selected_t1_node.value
    selected_t1_node.rightChild , selected_t2_node.rightChild = selected_t2_node.rightChild , selected_t1_node.rightChild
    selected_t1_node.leftChild , selected_t2_node.leftChild = selected_t2_node.leftChild , selected_t1_node.leftChild

    num1 = random.randint(0, 10000)
    if (num1<10): # Jahesh rokh midahad
        NewTree1 = Jahesh(NewTree1)

    num1 = random.randint(0, 10000)
    if (num1<10): # Jahesh rokh midahad
        NewTree2 = Jahesh(NewTree2)    

    return NewTree1,NewTree2


def find_tree_outputs(tree,input_values):
    my_output= []
    myfunc = str(printTree(tree))
    
    for input in input_values:
        try:
            if not myfunc.__contains__('x'):
                my_output.append(eval(myfunc))
            else:
                result = myfunc.replace('x',str(input))
                my_output.append(eval(result))
        except:
            my_output.append(0)
    return my_output
    
def find_tree_estimate(all_trees,our_input,our_output):
    for tree in all_trees:
        tree_output = find_tree_outputs(tree,our_input)
        try:
            tree.MSE = mse(our_output,tree_output)
        except:
            tree.MSE = 1_000_000_000

def CreatePopulation(size):
    population=[]
    operators = ['+','-','*','/','**','math.sin','math.cos']
    numbers = [1,2,3,4,5,6,7,8,9,10]
    # variables = [x,y,z,.....]

    for i in range(0,size):
        operator = random.choice(operators)
        number = random.choice(numbers)
        # variable = random.choice(variables)
        mainNode = node(operator)
        mainNode.leftChild = node('x',mainNode)  # we can change it with node(variable)
        if operator!='sin' or operator!='cos':
            mainNode.rightChild = node(number,mainNode)
        population.append(mainNode)
    find_tree_estimate(population,input_values,output_values)
    return population

def createNextGeneration(population,size_of_next_generation):
    my_list =[]

    for i in range(size_of_next_generation//2):
        randomChoises = random.sample(population,2)
        newT1,newT2 = combineTrees(randomChoises[0],randomChoises[1])
        my_list.append(newT1)
        my_list.append(newT2)
    find_tree_estimate(my_list,input_values,output_values)
    return my_list




def unique(list1):
    unique_list = [list1[0]]
    unique_list_str = [printTree(list1[0])]
    l = len(list1)
    # traverse for all elements
    for i in range(1,l):
        selectedtree = printTree(list1[i])
        if not unique_list_str.__contains__(selectedtree):
            unique_list.append(list1[i])
            unique_list_str.append(selectedtree)
    return unique_list


def functiontest(input):
    result=[]
    for i in input:
        result.append(i**4+10*i+math.sin(i))
    return result

input_values =[1,2,3,4,5,6,7,8,9]
output_values = functiontest(input_values)

size_of_population = 20
size_of_next_generation = 80
number_of_generation = 7

generations = []
best_mse=[]

for i in range (number_of_generation+1):
    generations.append(i)

population = CreatePopulation(size_of_population)
population= sorted(population, key=lambda node: node.MSE)
best_mse.append(population[0].MSE)
print("MY first population :")
for p in population:
    print(str(printTree(p))+"\t MSE : "+str(p.MSE))

for i in range(number_of_generation):
    print("\n\nMY "+str(i+1)+" population :")
    next_gen = createNextGeneration(population,size_of_next_generation)
    population.extend(next_gen)
    # population.sort(key=lambda x: abs(x.MSE))
    population = unique(population)
    sorted_nodes = sorted(population, key=lambda node: node.MSE)
    
    if sorted_nodes[0].MSE <0.6:
        print("OUR FINAL RESULT = "+str(printTree(sorted_nodes[0])))
        break
    
    population = sorted_nodes[:size_of_population]
    best_mse.append(population[0].MSE)

    # for p in population:
    #     print(str(printTree(p))+"\t MSE : "+str(p.MSE))

print(generations)
print(best_mse)
xpoints = np.array(generations)
ypoints = np.array(best_mse)
plt.plot(xpoints, ypoints)
plt.show()