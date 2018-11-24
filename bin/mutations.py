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

def rebind_variable(cand, variable_list):
  cand_node = cand.get_node()
  
  name_num = 0
  for node in ast.walk(cand_node):
    if isinstance(node, ast.Name):
      name_num += 1

  if name_num <= 0:
    return None

  input_name = random.sample(variable_list, 1)[0]
  change_num = random.randrange(0, name_num)
  return changeName(input_name, change_num).visit(cand_node)

def fix_off_by_one(cand):
  return

def replace_variable_with_constant(cand, max_const):
  return

def delete_statement(cand):
  return

def insert_new_statement(cand, cand_list):
  return
