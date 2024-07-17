class Node:
   def __init__(self, dataval=None, dataUID=None):
      self.dataval = dataval
      self.dataUID = dataUID
      self.nextval = None
      self.prevval = None

class SLinkedList:
   def __init__(self):
      self.headval = None
      self.tailval = None

   def AddEnd(self, newdata, newID):
      NewNode = Node(newdata, newID)
      if self.headval is None:
         self.headval = NewNode
         self.tailval = NewNode
         return
      NewNode.prevval = self.tailval
      self.tailval.nextval = NewNode
      self.tailval = NewNode

   # def AddEnd(self, newdata):
   #    NewNode = Node(newdata)
   #    if self.headval is None:
   #       self.headval = NewNode
   #       return
   #    laste = self.headval
   #    while(laste.nextval):
   #       laste = laste.nextval
   #    laste.nextval=NewNode

   def remove(self, node):
      # deleting the first node
      if node.prevval is None and node.nextval is None:
         self.headval = None
         self.tailval = None
      elif node.prevval is None:# node.prevval = None
         self.headval = node.nextval
         self.headval.prevval = None
      # deleting the last node
      elif node.nextval is None:
         self.tailval = node.prevval
         node.prevval.nextval = None
      else:
         node.prevval.nextval = node.nextval
         node.nextval.prevval = node.prevval
         # print("middle")
         

   def listprint(self):
      printval = self.headval
      count = 0
      while printval is not None:
         count += 1
         print (printval.dataval, " - UID = ", printval.dataUID)
         printval = printval.nextval
         # if count == 11:
         #    break
         #    exit()

   def length(self):
        """ Return the number of nodes in the list """
        current_node = self.headval
        count = 0
        while current_node:
            count += 1
            current_node = current_node.nextval
        return count