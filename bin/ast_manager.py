import astor
import ast
import os
from functools import reduce
from read import get_fn_in_direc
from evo_search import codeCand
from copy import deepcopy

# class changeFuncNames(ast.NodeTransformer):
#   def __init__(self, fn):
#     ast.NodeTransformer.__init__(self)
#     self.fn = fn

#   def visit_FunctionDef(self, node):
#     node.name = f"{node.name}_{self.fn}"
#     return node

class fillHoleNode(ast.NodeTransformer):
  def __init__(self, switch_node):
    ast.NodeTransformer.__init__(self)
    self.sw_n = switch_node

  def visit_Assign(self, node):
    if (len(node.targets) > 0):
      first = node.targets[0]
      if (isinstance(first, ast.Name) and first.id == '__HOLE__'):
        return self.sw_n
    return node

class addSuffixFuncdef(ast.NodeTransformer):
  def __init__(self, suffix, funcs):
    ast.NodeTransformer.__init__(self)
    self.suffix = suffix
    self.funcs = funcs

  def visit_FunctionDef(self, node):
    if (node.name in self.funcs):
      node.name += self.suffix
      for n in node.body:
        addSuffixFuncdef(self.suffix, self.funcs).visit(n)
    return node

  def visit_Call(self, node):
    if (not isinstance(node.func, ast.Attribute)) and (node.func.id in self.funcs):
      node.func.id += self.suffix
    return node

'''
add_suffix_to_funcdef
input: ast root node, string for suffix
output: ast root node
'''
def add_suffix_to_funcdef(tree, suffix):
  func_names = []
  for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
      func_names.append(node.name)
  return addSuffixFuncdef(suffix, func_names).visit(tree)

'''
Func for generating candidates
input: code_direc
ouput: dict (file name: ast Node), dict (file name: funcDef Node)
'''
def generate_candidates(code_direc):
  # Constants
  CAND_NODES = [ast.AnnAssign, ast.Assign,
                ast.For, ast.Call, ast.If, ast.While]

  # Declare variables
  fns = get_fn_in_direc(code_direc)
  func_dict = {}
  cand_list = []

  for fn in fns:
    splited_name = fn.split('.')

    if splited_name[-1] != 'py':
      continue

    name = splited_name[0]

    # Parse code into ast tree
    tree = astor.code_to_ast.parse_file(os.path.join(code_direc, fn))

    # Add suffix to func names
    tree = add_suffix_to_funcdef(tree, f"_{name}")

    # Get func_names
    for node in ast.walk(tree):
      # has_input = False
      # for inner in ast.walk(node):
      #   if isinstance(inner, ast.Name) and (inner.id == 'input' or inner.id == 'stdin'):
      #     has_input = True
      #     break
      #   elif isinstance(inner, ast.Attribute) and (inner.attr == 'stdin'):
      #     has_input = True
      #     break
      
      # if has_input:
      #   continue

      if isinstance(node, ast.FunctionDef):
        func_dict[node.name] = node
      elif reduce(lambda x, y: x or y,
                list(map(lambda x: isinstance(node, x), CAND_NODES))):
        cand_list.append(codeCand(node, name))

  return cand_list, func_dict

'''
Switch __HOLE__ with input node
input: codeCand, ast tree, list of ast nodes
output: string of code
'''
def fill_hole(cand, holed_node, func_dict):
  cand_node = cand.get_node()
  func_name_list = []
  for node in ast.walk(cand_node):
    if isinstance(node, ast.Call):
      if isinstance(node.func, ast.Name) and (node.func.id in func_dict.keys()):
        func_name_list.append(node.func.id)
  
  module_body = []
  for func_name in list(set(func_name_list)):
    module_body.append(func_dict[func_name])
  module_body.append(cand_node)

  input_node = ast.Module(body=module_body)
  filled_node = fillHoleNode(input_node).visit(deepcopy(holed_node))
  return astor.to_source(filled_node)

'''
get_name_list
input: ast tree
output: list of string
'''
def get_name_list(tree):
  name_list = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
      for inner_node in node.targets:
        if isinstance(inner_node, ast.Name):
          name = inner_node.id
          if name not in name_list and name != "__HOLE__":
            name_list.append(name)
    elif isinstance(node, ast.For):
      name = node.target.id
      if name not in name_list and name != "__HOLE__":
        name_list.append(name)
    elif isinstance(node, ast.FunctionDef):
      for arg in node.args.args:
        name = arg.arg
        if name not in name_list and name != "__HOLE__":
          name_list.append(name)
  return name_list

'''
get_max_val
input: ast tree
output: integer
'''
def get_max_val(tree):
  maximum = None
  for node in ast.walk(tree):
    if isinstance(node, ast.Num):
      if maximum == None or maximum < node.n:
        maximum = node.n
  return maximum
