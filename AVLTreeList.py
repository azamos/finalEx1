# username - amoszohar
# id1      - 311402812
# name1    - amos zohar
# id2      - None
# name2    - None

from random import randrange

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1  # Balance factor
        self.size = 0

    def setAsVirtualNode(self):
        self.value = None
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    def initiateAsLeaf(self, val):
        leftVirtualSon = AVLNode(None)
        rightVirtualSon = AVLNode(None)
        self.setValue(val)
        self.setLeft(leftVirtualSon)
        self.setRight(rightVirtualSon)
        leftVirtualSon.setParent(self)
        rightVirtualSon.setParent(self)
        self.setHeight(0)
        self.setSize(1)

    def isLeaf(self):
        return self.getRight().isRealNode() is False and self.getLeft().isRealNode() is False

    def getSize(self):
        return self.size

    def setSize(self, s):
        self.size = s

    def isLeftSon(self):
        return self.getParent() and self.getParent().getLeft() is self

    def isRightSon(self):
        return self.getParent() and self.getParent().getRight() is self

    def getBalanceFactor(self):
        return self.getLeft().getHeight() - self.getRight().getHeight()
    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if self.left is None:
            return None
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if self.right is None:
            return None
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        if self.parent is None:
            return None
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        if self.isRealNode() is False:
            return None
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.value is not None


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        self.root = None
    # add your fields here
        self.firstListItem = None
        self.lastListItem = None
    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        return self.treeSelect(i).getValue()

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        newNode = AVLNode(val)
        newNode.initiateAsLeaf(val)
        fixFromNode = newNode
        if i == 0:
            self.firstListItem = newNode
        if self.empty():
            self.root = newNode
            self.lastListItem = newNode
            self.firstListItem = newNode
        elif i == self.size-1:
            x = self.last()
            x.setRight(newNode)
            newNode.setParent(x)
            self.lastListItem = newNode
        elif i < self.size:
            currentListAtIndex = self.treeSelect(i)
            if currentListAtIndex.getLeft().isRealNode() is False:
                currentListAtIndex.setLeft(newNode)
                newNode.setParent(currentListAtIndex)
            else:
                pred = self.predecessor(currentListAtIndex)
                predRight = pred.getRight()
                pred.setRight(newNode)
                newNode.setParent(pred)
                newNode.setRight(predRight)
                predRight.setParent(newNode)
        self.size += 1
        #fixFromNode.setSize(fixFromNode.getSize()+1)
        self.resizeAndReheight(fixFromNode)
        return self.rebalanceTreeFromNode(fixFromNode)


    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        nodeToBeDeleted = self.treeSelect(i)
        """"First, dealing with edge cases"""
        if nodeToBeDeleted is self.root:
            if self.size == 1:
                self.root = None
                self.size = 0
                self.firstListItem = None
                self.lastListItem = None
                return 0
        """"
            Part 1: regular binary search tree deletion.
        """
        """"Determine node to replace the original one"""
        replacer = self.successor(nodeToBeDeleted)
        if replacer is None:
            replacer = self.predecessor(nodeToBeDeleted)
        """"connecting to the replacement, and keeping references to them so I can make them the replacement's
            children, after disconnecting him from his original location in the tree"""
        leftSonOfNode = nodeToBeDeleted.getLeft()
        leftSonOfNode.setParent(replacer)
        rightSonOfNode = nodeToBeDeleted.getRight()
        rightSonOfNode.setParent(replacer)
        sizeOfNodeTobeDeleted = nodeToBeDeleted.getSize()
        """"
            Disconnect Replacer from it's location in the tree,
            Without ruining the structure of the tree
        """
        replacerRightSon = replacer.getRight()
        replacerLeftSon = replacer.getLeft()
        replacerParent  = replacer.getParent()
        if replacerRightSon.isRealNode():
            if replacerParent is not None:
                replacer.setRight(replacerRightSon)
                replacerParent.setSize(replacerParent.getSize()-1)
            replacerRightSon.setParent(replacerParent)
        elif replacerLeftSon.isRealNode():
            if replacerParent is not None:
                replacerParent.setLeft(replacerLeftSon)
                replacerParent.setSize(replacerParent.getSize() - 1)
            replacerLeftSon.setParent(replacerParent)
        """"
            Now, it remains to just define replacer sons
        """
        replacer.setLeft(leftSonOfNode)
        replacer.setRight(leftSonOfNode)
        replacer.setSize(sizeOfNodeTobeDeleted)
        """"
            End of part 1: regular binary search tree deletion
        """
        """"
            Part 2: fixing the size attribute where needed, and validating AVl rule.
            If not compliant, perform rebalances as required.
        """
        fixSizeAndBFFromHereUptoRoot = replacerParent if replacerParent.getRight().isRealNode() else replacer
        x = fixSizeAndBFFromHereUptoRoot
        while x is not self.root:
            x.setSize(x.getSize()-1)

        rotations = self.rebalanceTreeFromNode(fixSizeAndBFFromHereUptoRoot)
        return rotations

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.firstListItem is None:
            return None
        return self.firstListItem

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return self.lastListItem

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        arr = [""] * self.size
        p = self.minimum
        while (not p is None) and p.isRealNode():
            arr[p.getRank()] = str(p.getValue())
            p = self.successor(p)
        return arr

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        sortedArr = self.quickSort(self.listToArray())
        sortedAVLlist = AVLTreeList()
        n = len(sortedArr)
        for i in range(n):
            sortedAVLlist.insert(sortedArr[i])

    def quickSort(self, arr):
        pIndex = randrange(0, arr.size())
        pivot = arr[pIndex]
        smallerElements = []
        equalElemens = []
        biggerElements = []
        for info in arr:
            if info < pivot:
                smallerElements.append(info)
            elif info == pivot:
                equalElemens.append(info)
            elif info > pivot:
                biggerElements.append(info)
        return self.quickSort(smallerElements) + equalElemens + self.quickSort(biggerElements)

    """permute the info values of the list 

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        arr = self.listToArray()
        n = len(arr)
        permutatonTheta = AVLTreeList()
        wasAllreadyRolled = [False] * n
        i = 0
        while i < n:
            randRes = randrange(n)
            if wasAllreadyRolled[randRes] == False:
                permutatonTheta.insert(0, arr[randRes])
                wasAllreadyRolled[randRes] = True
                i += 1
        return permutatonTheta

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        leftTree = self
        rightTree = lst
        x = rightTree.first()
        pointerTree2 = x.getParent()
        x.setParent(None)
        virtSon = AVLNode(None)
        virtSon.setAsVirtual()
        pointerTree2.setLeft(virtSon)
        delta = rightTree.size - leftTree.size
        if delta > 0:
            x.setLeft(leftTree.root)
            while pointerTree2.getHeight() > leftTree.root.getHeight():
                pointerTree2 = pointerTree2.getParent()
            x.setParent(pointerTree2.getParent())
            pointerTree2.getParent().setLeft(x)
            pointerTree2.setParent(x)
            self.rebalanceTree(x)
        if delta == 0:
            x.setLeft(leftTree.root)
            x.setRight(rightTree.root)
            leftTree.setParent(x)
            rightTree.setParent(x)
        if delta < 0:
            x = 5

        return abs(delta)

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        x = self.first()
        while x is not self.last():
            if x.getValue() == val:
                return x.getRank() - 1
        return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

    """"
        Auxiliary functions start here                                
    """

    def subtreeSelect(self, node, k):
        r = node.getLeft().getSize() + 1
        if k == r:
            return node
        elif k < r:
            return self.subtreeSelect(node.getLeft(), k)
        elif k > r:
            return self.subtreeSelect(node.getRight(), k - r)

    """"In place of retrieve(L,i)"""
    def treeSelect(self, k):
        if k > self.size or k < 0:
            return None
        return self.subtreeSelect(self.root, k)

    def select(self, k):
        x = self.first()
        while x.getSize() < k:
            x = x.getParent()
        return self.treeSelect(k)

    """"In place of getRank(L,node)"""
    def treeRank(self,node):
        counter = 1
        x = node
        while x is not None:
            if not x.isLeftSon():
                counter += 1 + x.getLeft().getSize()
        return counter

    def successor(self, node):
        if node is self.last():
            return None
        if node.getRight().isRealNode():
            return self.findMinInSubTree(node.getRight())
        ancestor = node.getParent()
        while ancestor.getParent() is not None:
            if ancestor.isRightSon():
                return ancestor
            ancestor = ancestor.getParent()
        return None

    def findMinInSubTree(self, node):
        x = node
        while x.isRealNode():
            x = x.getLeft()
        return x

    def predecessor(self, node):
        if node is self.first():
            return None
        if node.getLeft().isRealNode():
            return self.findMaxInSubtree(node.getLeft())
        ancestor = node.getParent()
        while ancestor.getParent() is not None:
            if ancestor.isLeftSon():
                return ancestor
            ancestor = ancestor.getParent()
        return None

    def findMaxInSubtree(self, node):
        x = node
        while x.isRealNode():
            x = x.getRight()
        return x

    def rebalanceTreeFromNode(self, node):
        rebalances = 0
        p = node
        while not p is None:
            if abs(p.getBalanceFactor()) > 1:
                rebalances += self.determineOperationAndExecute(p)
            p = p.getParent()
        return rebalances

    def determineOperationAndExecute(self, criminalNode):
        counter = 0;
        bf = criminalNode.getBalanceFactor()
        if bf == -2:
            rightChildBalanceFactor = criminalNode.getRight().getBalanceFactor()
            if rightChildBalanceFactor == 1:
                self.rotateRight(criminalNode)
                counter += 1
            self.rotateLeft(criminalNode)
        if bf == 2:
            leftChildBalanceFactor = criminalNode.getRight().getBalanceFactor()
            if leftChildBalanceFactor == -1:
                self.rotateLeft(criminalNode)
                counter += 1
            self.rotateRight(criminalNode)
        counter += 1
        return counter

    def rotateLeft(self, criminalNode):
        rightSonOfCriminal = criminalNode.right
        newRightSonOfProblemNode = rightSonOfCriminal.left
        parent = criminalNode.parent
        if criminalNode is parent.right:
            parent.right = rightSonOfCriminal
        elif criminalNode is parent.left:
            parent.left = rightSonOfCriminal
        criminalNode.parent = rightSonOfCriminal
        rightSonOfCriminal.parent = parent
        newRightOfCriminal = rightSonOfCriminal.left
        rightSonOfCriminal.left = criminalNode
        criminalNode.right = newRightOfCriminal

        rightSonOfCriminal.setSize(criminalNode.getSize())
        criminalNode.setSize(newRightSonOfProblemNode.getSize()+criminalNode.getLeft().getSize()+1)

    def rotateRight(self, criminalNode):
        leftSonOfCriminal = criminalNode.left
        newLeftSonOfProblemNode = leftSonOfCriminal.right
        parent = criminalNode.parent
        if criminalNode is parent.right:
            parent.right = leftSonOfCriminal
        elif criminalNode is parent.left:
            parent.left = leftSonOfCriminal
        criminalNode.parent = leftSonOfCriminal
        leftSonOfCriminal.parent = parent
        newLeftOfCriminal = leftSonOfCriminal.right
        leftSonOfCriminal.right = criminalNode
        criminalNode.left = newLeftOfCriminal

        leftSonOfCriminal.setSize(criminalNode.getSize())
        criminalNode.setSize(newLeftSonOfProblemNode.getSize()+criminalNode.getRight().getSize()+1)

    def resizeAndReheight(self,node):
        self.updateHeightsInPath(node)
        x = node
        while x is not None:
            x.setSize(x.getSize()+1)
            x = x.getParent()

    def updateHeightsInPath(self,node):
        while node is not self.root:
            node.setSize(1+max(node.getLeft().getHeight(),node.getRight().getHeight()))
            node = node.getParent()

""""
    Testing grounds
"""

testList = AVLTreeList()
testList.insert(0,"asgasgagg")
print(testList.retrieve(0))



