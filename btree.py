from __future__ import annotations
import json
import math
from typing import List

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.children = children
        self.parent   = parent

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = None

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "k": node.keys,
                "c": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int):
        if self.root == None:
            self.root = Node(keys = [key], children = [None, None], parent = None)
        else:
            self.insertHelp(self.root, key, self.m)

    def insertHelp(self, curr:Node, key: int, m: int):
        if curr.children != None and self.isEmpty(curr.children) == False:
            for idx, x, in enumerate(curr.keys):
                if x > key:
                    self.insertHelp(curr.children[idx], key, m)
                    self.rebalance(curr, m)
                    return
            self.insertHelp(curr.children[len(curr.keys)], key, m)
            self.rebalance(curr, m)
        else:
            self.insertInPlace(curr.keys, key)
            if curr.children == None:
                curr.children = [None, None]
            else:
                curr.children = curr.children + [None]
            self.rebalance(curr, m)

    def isEmpty(self, list: List):
        for x in list:
            if x != None:
                return False
        return True
        

    def rebalance(self, curr:Node, m:int):
        if len(curr.keys) >= m:
            if curr.parent == None:
                curr.parent = Node(keys = [], children = [curr], parent = None)
                self.root = curr.parent
                self.split(curr, m)


                # half = math.ceil(m/2)
                # newLeft = curr.keys[:half-1]
                # newRight = curr.keys[half:]
                # if curr.children == None:
                #     leftChildren = []
                #     rightChildren = []
                # else:
                #     leftChildren = curr.children[:half]
                #     rightChildren = curr.children[half:]
                #     if self.isEmpty(rightChildren):
                #         rightChildren.append(None)
                # leftChild = Node(keys = newLeft, children = [leftChildren], parent = curr)
                # rightChild = Node(keys = newRight, children = [rightChildren], parent = curr)
                # curr.keys = [curr.keys[half-1]]
                # curr.children = [leftChild, rightChild]
            else:
                idx = curr.parent.children.index(curr)
                if idx-1 >= 0 and len(curr.parent.children[idx-1].keys) < m-1:
                    self.rotateLeft(curr)
                elif idx+1 < len(curr.parent.children) and len(curr.parent.children[idx+1].keys) < m-1:
                    self.rotateRight(curr)
                else:
                    self.split(curr, m)
        elif len(curr.keys) <= (math.ceil(m/2) -2) and curr != self.root:
            idx = curr.parent.children.index(curr)
            # print(idx)
            # print(len(curr.parent.children))
            # print(curr.parent.children[idx+1].keys)
            if idx-1 >= 0 and len(curr.parent.children[idx-1].keys) >= math.ceil(m/2):
                self.rotateRight(curr.parent.children[idx-1])
            elif idx+1 < len(curr.parent.children) and len(curr.parent.children[idx+1].keys) >= math.ceil(m/2):
                self.rotateLeft(curr.parent.children[idx+1])
            else:
                if idx-1 >= 0:
                    self.mergeLeft(curr)
                else:
                    self.mergeRight(curr)

    def insertInPlace(self, list: List, key):
        for idx, x, in enumerate(list):
            if x > key:
                list.insert(idx, key)
                return
        list.insert(len(list), key)

    # Delete.
    def delete(self, key: int):
        # Fill in the details.
        if len(self.root.keys) == 1 and (self.root.children == None or self.isEmpty(self.root.children)):
            self.root = None
        else:
            self.deleteHelp(self.root, key, self.m)

    def deleteHelp(self, curr:Node, key, m):
        if key in curr.keys:
            idx = curr.keys.index(key)
            if curr.children != None:
                if self.isEmpty(curr.children):
                    curr.keys.remove(key)
                    curr.children = curr.children[1:]
                    self.rebalance(curr, m)
                else:
                    temp = self.inOrderSucc(curr.children[idx+1])
                    curr.keys[idx] = temp
                    #print(curr.keys)
                    self.deleteHelp(curr.children[idx+1], temp, m)
                    #print(curr.keys)
                    self.rebalance(curr, m)
        else:
            for idx, x, in enumerate(curr.keys):
                if x > key:
                    self.deleteHelp(curr.children[idx], key, m)
                    self.rebalance(curr, m)
                    return
            self.deleteHelp(curr.children[len(curr.keys)], key, m)
            self.rebalance(curr, m)
    
    def inOrderSucc(self, curr: Node):
        if self.isEmpty(curr.children):
            return curr.keys[0]
        return self.inOrderSucc(curr.children[0])

    # Search
    def search(self,key) -> str:
        list = "["
        list = self.searchHelp(self.root, key, list)
        if len(list) > 2:
            list = list[:len(list)-2]
        list = list + "]"
        return list
        
    def searchHelp(self, curr: Node, key, acc):
        if key in curr.keys:
            return acc
        else:
            for idx, x, in enumerate(curr.keys):
                if x > key:
                    acc = acc + str(idx) + ", "
                    return self.searchHelp(curr.children[idx], key, acc)
            idx = len(curr.children)-1
            acc = acc + str(idx) + ", "
            return self.searchHelp(curr.children[idx], key, acc)

    
    def rotateRight(self, curr : Node):
        temp = curr.keys.pop(len(curr.keys)-1)
        idx = curr.parent.children.index(curr)
        temp2 = curr.parent.keys[idx]
        curr.parent.keys[idx] = temp
        sibling = curr.parent.children[idx+1]
        # if sibling.keys == None:
        #     sibling.keys = []
        sibling.keys.insert(0, temp2)
        # if curr.children != None and curr.children!= []:
        #     if sibling.children == None:
        #         sibling.children = []
        sibling.children.insert(0, curr.children.pop(len(curr.children)-1))
        if sibling.children[0] != None:
            sibling.children[0].parent = sibling

    def rotateLeft(self, curr : Node):
        temp = curr.keys.pop(0)
        idx = curr.parent.children.index(curr)
        temp2 = curr.parent.keys[idx-1]
        curr.parent.keys[idx-1] = temp
        sibling = curr.parent.children[idx-1]
        # if sibling.keys == None:
        #     sibling.keys = []
        sibling.keys.append(temp2)
        # if curr.children != None and curr.children!= []:
        #     if sibling.children == None:
        #         sibling.children = []
        sibling.children.append(curr.children.pop(0))
        if sibling.children[len(sibling.children)-1] != None:
            sibling.children[len(sibling.children)-1].parent = sibling

    def split(self, curr: Node, m: int):
        half = math.ceil(m/2)
        newLeft = curr.keys[:half-1]
        newRight = curr.keys[half:]
        idx = curr.parent.children.index(curr)
        curr.parent.keys.insert(idx, curr.keys[half-1])
        # if curr.children != None:
        newChildren = curr.children[half:]
        if self.isEmpty(newChildren):
            newChildren = [None] * (len(newRight)+1)
        # else:
        #     newChildren = None
        curr.keys = newLeft
        newSib = Node(keys = newRight, children = newChildren, parent = curr.parent)
        curr.parent.children.insert(idx+1, newSib)
        for idx, x, in enumerate(curr.children):
            if idx >= half:
                if x != None:
                    x.parent = newSib
            else:
                if x != None:
                    x.parent = curr
        curr.children = curr.children[:half]
    
    def mergeLeft(self, curr: Node):
        idx = curr.parent.children.index(curr)
        temp = curr.parent.keys[idx-1]
        sibling = curr.parent.children[idx-1]
        if sibling.keys == None:
            sibling.keys = []
        if sibling.children == None:
            sibling.children = []
        if curr.children == None:
            curr.children = []
        if self.isEmpty(curr.children) == False:
            for x in curr.children:
                x.parent = sibling
        sibling.keys = sibling.keys+[temp]+curr.keys
        sibling.children = sibling.children+curr.children
        if self.isEmpty(sibling.children):
            sibling.children = [None] * (len(sibling.keys)+1)
        curr.parent.keys.pop(idx-1)
        curr.parent.children.pop(idx)

    def mergeRight(self, curr: Node):
        idx = curr.parent.children.index(curr)
        temp = curr.parent.keys[idx]
        sibling = curr.parent.children[idx+1]
        if sibling.keys == None:
            sibling.keys = []
        if sibling.children == None:
            sibling.children = []
        if curr.children == None:
            curr.children = []
        if self.isEmpty(curr.children) == False:
            for x in curr.children:
                x.parent = sibling
        sibling.keys = curr.keys+[temp]+sibling.keys
        sibling.children = curr.children+sibling.children
        if self.isEmpty(sibling.children):
            sibling.children = [None] * (len(sibling.keys)+1)
        curr.parent.keys.pop(idx)
        curr.parent.children.pop(idx)
