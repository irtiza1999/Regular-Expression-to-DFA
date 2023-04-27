class Stack:
    def __init__(self):
        self.stackList = []

    def push(self, value):
        self.stackList.append(value)

    def pop(self):
        if self.stackList:
            return self.stackList.pop()

    def isempty(self):
        return not bool(self.stackList)


def reToPostfix(re):
    re = re+".#"
    outStr = ''
    myStack = Stack()
    precedence = {"|": 1, ".": 2, "*": 3, "(": 0, ")": 0}
    for i in range(len(re)):
        if re[i].isalnum() or re[i] == "#":
            outStr += re[i]
        else:
            if myStack.isempty():
                myStack.push(re[i])
            else:
                if re[i] == "(":
                    myStack.push(re[i])
                elif re[i] == ")":
                    while myStack.stackList[-1] != "(":
                      outStr += myStack.pop()
                    myStack.pop()
                elif precedence[myStack.stackList[-1]] < precedence[re[i]]:
                    myStack.push(re[i])
                elif precedence[myStack.stackList[-1]] >= precedence[re[i]]:
                    while precedence[myStack.stackList[-1]] >= precedence[re[i]]:
                        outStr += myStack.pop()
                        if myStack.isempty():
                            break
                    myStack.push(re[i])
    while not myStack.isempty():
        outStr += myStack.pop()
    return outStr

augList = {}
def build_syntax_tree(x):
    myList = []
    nodes = {}
    count = 1
    for i in x:
        if i.isalnum() or i == "#":
            myList.append((i, count))
            if i in augList.keys():
              augList[i].append(count)
            else:
              augList[i] = [count]
            count += 1
        else:
            myList.append(i)
    count = 1
    while len(myList) > 1:
        for i in range(len(myList)):
            if myList[i] in [".", "|"]:
                nodes[(myList[i], count)] = [[myList[i-2], myList[i-1]]]
                myList = myList[:i-2] + [(myList[i], count)] + myList[i+1:]
                count += 1
                break
            elif myList[i] == "*":
                nodes[(myList[i], count)] = [[myList[i-1]]]
                myList = myList[:i-1] + [(myList[i], count)] + myList[i+1:]
                count += 1
                break
    return nodes, myList[0]

def nullable(tree, node):
    if node not in tree:
        return False
    else:
        if node[0] =="|":
            left=nullable(tree, tree[node][0][0])
            right=nullable(tree, tree[node][0][1])
            tree[node].append(left or right)
            return left or right
        elif node[0] ==".":
            left=nullable(tree, tree[node][0][0])
            right=nullable(tree, tree[node][0][1])
            tree[node].append(left and right)
            return left and right
        elif node[0] =="*":
            nullable(tree, tree[node][0][0])
            tree[node].append(True)
            return True

def nullableCheck(tree, node):
    if node not in tree:
        return False
    else:
        if node[0] =="|":
            left=nullableCheck(tree, tree[node][0][0])
            right=nullableCheck(tree, tree[node][0][1])
            return left or right
        elif node[0] ==".":
            left=nullableCheck(tree, tree[node][0][0])
            right=nullableCheck(tree, tree[node][0][1])
            return left and right
        elif node[0] =="*":
            return True

def firstpos(tree, node): #(a,1)
    if node not in tree:
        return {node[1]}
    else:
        result = set()
        if node[0] == "|":
            left = firstpos(tree, tree[node][0][0])
            right = firstpos(tree, tree[node][0][1])
            result.update(left)
            result.update(right)
            tree[node].append(result)
            return result
        elif node[0] == ".":
            left = firstpos(tree, tree[node][0][0])
            leftNull = nullableCheck(tree, tree[node][0][0])
            right = firstpos(tree, tree[node][0][1])
            if leftNull == True:
                result.update(left)
                result.update(right)
            else:
                result.update(left)
            tree[node].append(result)
            return result
        else:
            result.update(firstpos(tree, tree[node][0][0]))
            tree[node].append(result)
            return result

def firstposCheck(tree, node):
    if node not in tree:
        return {node[1]}
    else:
        result = set()
        if node[0] == "|":
            left = firstposCheck(tree, tree[node][0][0])
            right = firstposCheck(tree, tree[node][0][1])
            result.update(left)
            result.update(right)
            return result
        elif node[0] == ".":
            left = firstposCheck(tree, tree[node][0][0])
            leftNull = nullableCheck(tree, tree[node][0][0])
            right = firstposCheck(tree, tree[node][0][1])
            if leftNull == True:
                result.update(left)
                result.update(right)
            else:
                result.update(left)
            return result
        else:
            result.update(firstposCheck(tree, tree[node][0][0]))
            return result

def lastpos(tree, node):
    if node not in tree:
        return {node[1]}
    else:
        if node[0] == "|":
            left = lastpos(tree, tree[node][0][0])
            right = lastpos(tree, tree[node][0][1])
            result = left.union(right)
            tree[node].append(result)
            return result
        elif node[0] == ".":
            left = lastpos(tree, tree[node][0][0])
            right = lastpos(tree, tree[node][0][1])
            rightNull = nullableCheck(tree, tree[node][0][1])
            if rightNull == True:
                result = left.union(right)
                tree[node].append(result)
                return result
            else:
                result = right
                tree[node].append(result)
                return result
        else:
            result = lastpos(tree, tree[node][0][0])
            tree[node].append(result)
            return result

def lastposCheck(tree, node):
    if node not in tree:
        return {node[1]}
    else:
        if node[0] == "|":
            left = lastposCheck(tree, tree[node][0][0])
            right = lastposCheck(tree, tree[node][0][1])
            result = left.union(right)
            return result
        elif node[0] == ".":
            left = lastposCheck(tree, tree[node][0][0])
            right = lastposCheck(tree, tree[node][0][1])
            rightNull = nullableCheck(tree, tree[node][0][1])
            if rightNull == True:
                result = left.union(right)
                return result
            else:
                result = right
                return result
        else:
            result = lastposCheck(tree, tree[node][0][0])
            return result

def giveChar(num, augList):
  for key, value in augList.items():
    for k in value:
      if num == k:
        return key, num

def print_node_info(tree, node):
    # print node value
    print(f"Node: {node[0]}")

    # print nullable status
    nullable = tree[node][-3]
    print(f"Nullable: {nullable}")

    # print firstpos
    firstpos = tree[node][-2]
    print(f"Firstpos: {firstpos}")

    # print lastpos
    lastpos = tree[node][-1]
    print(f"Lastpos: {lastpos}\n")


def followpos(tree):
    followTable = {}
    for node in tree:
      if node[0] == ".":
          leftLast = lastposCheck(tree, tree[node][0][0])
          rightFirst = firstposCheck(tree, tree[node][0][1])
          for i in leftLast:
            if i not in followTable.keys():
                followTable[i] = []
            for j in rightFirst:
              if j not in followTable[i]:
                  followTable[i].append(j)
      if node[0] == "*":
          nodeFirst = tree[node][-2]
          nodeLast = tree[node][-1]
          for i in nodeLast:
            if i not in followTable.keys():
                followTable[i] = []
            for j in nodeFirst:
              if j not in followTable[i]:
                  followTable[i].append(j)
      else:
          pass
      for value in augList.values():
        for i in value:
          if i not in followTable.keys():
            followTable[i] = []
    return followTable

#################################################

class queue: 
    def __init__(self):
        self.q = []
 
    def push(self,value):
        self.q += [value] 
        
    def pop(self):
        if self.q == []:
            return None 
        x = self.q[0]
        self.q = self.q[1:]
        return x

def create_DFA(followpos,re,start_node):
    DFA={}
    q1=queue()
    leafnode={}
    transitions={}
    c=1
    for i in re:
        if (ord("a") <=ord(i)<= ord("z")) or i=="#":
            leafnode[c]=i
            if i not in transitions and i !="#":
                transitions[i] = []
            c+=1
    q1.push(tuple(start_node))
    while q1.q !=[]:
        for i in transitions:
            transitions[i] = []
        if (q1.q[0] not in DFA) and (q1.q[0] != ()):
            DFA[q1.q[0]]= {}
            for i in q1.q[0]:
                if leafnode[i] != "#":
                    transitions[leafnode[i]] += [i]
            for k,v  in transitions.items():
                x=[]
                for i in v:
                    for j in followpos[i]:
                        if j not in x:
                            x += [j]
                x.sort()
                DFA[q1.q[0]][k]=tuple(x)
                q1.push(tuple(x))
            q1.pop()
        else:
            q1.pop()
    return DFA

def checkString(myStr, dfa, root):
    root = tuple(root)
    for i in range(len(myStr)):
      if myStr[i] not in augList:
        print("Illegal Charecter")
        return
      if dfa[root][myStr[i]]:
          nextState = dfa[root][myStr[i]]
          root = nextState
      else:
        print("String Not Accepted")
        return
    print("Final State:", nextState)
    for i in nextState:
        if i in augList["#"]:
            print("String Accepted")
            return
    print("String Not Accepted")
    return

re = "(a|b)*.a.b.b"
regex = reToPostfix(re)
augRe = re+".#"
tree, root = build_syntax_tree(regex)
null = nullable(tree, root)
first = firstpos(tree, root)
last = lastpos(tree, root)
follow = followpos(tree)
print("Tree:", tree,"\n")
for node in tree:
    print_node_info(tree, node)
print("FollowPos:", follow,"\n")
rootFirstPos = tree[root][2]
dfa = create_DFA(follow,augRe,rootFirstPos)
print("DFA:", dfa,"\n")
checkString("abb", dfa, rootFirstPos)
