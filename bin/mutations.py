import ast
import random
from copy import deepcopy
from functools import reduce

DELETE_TYPES = [ast.Module, ast.For, ast.While, ast.If]

class changeName(ast.NodeTransformer):
  def __init__(self, input_name, change_num):
    ast.NodeTransformer.__init__(self)
    self.input_name = input_name
    self.change_num = change_num
    self.name_num = 0

  def visit_Name(self, node):
    if (self.change_num == self.name_num):
      node.id = self.input_name
      self.name_num += 1
    elif (self.change_num > self.name_num):
      self.name_num += 1
    return node

class makeNumOff(ast.NodeTransformer):
  def __init__(self, change_num):
    ast.NodeTransformer.__init__(self)
    self.change_num = change_num
    self.name_num = 0

  def visit_Num(self, node):
    if (self.change_num == self.name_num):
      node.n = node.n - 1
      self.name_num += 1
    elif (self.change_num > self.name_num):
      self.name_num += 1
    return node

class changeNum(ast.NodeTransformer):
  def __init__(self, max_const, change_num):
    ast.NodeTransformer.__init__(self)
    self.max_const = max_const
    self.change_num = change_num
    self.name_num = 0

  def visit_Num(self, node):
    if (self.change_num == self.name_num):
      node.n = self.max_const
      self.name_num += 1
    elif (self.change_num > self.name_num):
      self.name_num += 1
    return node

class deleteOne(ast.NodeTransformer):
  def __init__(self, change_num):
    ast.NodeTransformer.__init__(self)
    self.change_num = change_num
    self.name_num = 0

  def visit(self, node):
    print(node)
    if reduce(lambda x, y: x or y,
              list(map(lambda x: isinstance(node, x), DELETE_TYPES))):
      if (len(node.body) >= 2):
        if (self.change_num == self.name_num):
          choice = random.choice(node.body)
          node.body.remove(choice)
          self.name_num += 1
        elif (self.change_num > self.name_num):
          self.name_num += 1
    return self.visit(node)

def rebind_variable(cand, variable_list):
  cand_node = cand.get_node()
  
  name_num = _count_type_nodes(cand_node, ast.Name)
  if name_num <= 0:
    return None

  input_name = random.sample(variable_list, 1)[0]
  change_num = random.randrange(0, name_num)
  new_node = changeName(input_name, change_num).visit(cand_node)
  return deepcopy(cand).set_node(new_node)


def fix_off_by_one(cand):
  cand_node = cand.get_node()

  node_num = _count_type_nodes(cand_node, ast.Num)
  if node_num <= 0:
    return None

  change_num = random.randrange(0, node_num)
  new_node = makeNumOff(change_num).visit(cand_node)
  return deepcopy(cand).set_node(new_node)

# TODO: fix...
def replace_variable_with_constant(cand, max_const):
  cand_node = cand.get_node()

  node_num = _count_type_nodes(cand_node, ast.Num)
  if node_num <= 0:
    return None

  change_num = random.randrange(0, node_num)
  new_node = changeNum(max_const, change_num).visit(cand_node)
  return deepcopy(cand).set_node(new_node)

def delete_statement(cand):
  cand_node = cand.get_node()

  node_num = _count_able_to_delete(cand_node, DELETE_TYPES)
  if node_num <= 0:
    return None

  delete_num = random.randrange(0, node_num)
  # TODO: fix deleteOne
  # return deleteOne(delete_num).visit(cand_node)
  return

def insert_new_statement(cand, cand_list):
  return

def refill(cand, cand_list):
  return random.choice(cand_list)

def _count_type_nodes(tree, ast_type):
  node_num = 0
  for node in ast.walk(tree):
    if isinstance(node, ast_type):
      node_num += 1
  return node_num

def _count_able_to_delete(tree, ast_types):
  node_num = 0
  for node in ast.walk(tree):
    if reduce(lambda x, y: x or y,
              list(map(lambda x: isinstance(node, x), ast_types))):
      if (len(node.body) >= 2):
        node_num += 1
  return node_num
