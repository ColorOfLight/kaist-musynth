import ast
import random

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

def rebind_variable(cand, variable_list):
  cand_node = cand.get_node()
  
  name_num = _count_type_nodes(cand_node, ast.Name)
  if name_num <= 0:
    return None

  input_name = random.sample(variable_list, 1)[0]
  change_num = random.randrange(0, name_num)
  return changeName(input_name, change_num).visit(cand_node)

def fix_off_by_one(cand):
  cand_node = cand.get_node()

  node_num = _count_type_nodes(cand_node, ast.Num)
  if node_num <= 0:
    return None

  change_num = random.randrange(0, node_num)
  return makeNumOff(change_num).visit(cand_node)

def replace_variable_with_constant(cand, max_const):
  cand_node = cand.get_node()

  node_num = _count_type_nodes(cand_node, ast.Num)
  if node_num <= 0:
    return None

  change_num = random.randrange(0, node_num)
  return changeNum(max_const, change_num).visit(cand_node)

def delete_statement(cand):
  return

def insert_new_statement(cand, cand_list):
  return

def _count_type_nodes(tree, ast_type):
  node_num = 0
  for node in ast.walk(tree):
    if isinstance(node, ast_type):
      node_num += 1
  return node_num
