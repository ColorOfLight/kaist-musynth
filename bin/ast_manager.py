import astor
import ast
import os
from functools import reduce
from read import get_fn_in_direc

# class changeFuncNames(ast.NodeTransformer):
#   def __init__(self, fn):
#     ast.NodeTransformer.__init__(self)
#     self.fn = fn

#   def visit_FunctionDef(self, node):
#     node.name = f"{node.name}_{self.fn}"
#     return node

class switchNode(ast.NodeTransformer):
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
  funcs_dict = {}
  cands_dict = {}

  for fn in fns:
    name = fn.split('.')[0]
    funcs = []
    cands = []

    # Parse code into ast tree
    tree = astor.code_to_ast.parse_file(os.path.join(code_direc, fn))

    # Add suffix to func names
    tree = add_suffix_to_funcdef(tree, f"_{name}")

    # Get func_names
    for node in ast.walk(tree):
      if isinstance(node, ast.FunctionDef):
        funcs.append(node)
      elif reduce(lambda x, y: x or y,
                list(map(lambda x: isinstance(node, x), CAND_NODES))):
        cands.append(node)
    
    funcs_dict[name] = funcs
    cands_dict[name] = cands

  return cands_dict, funcs_dict

'''
Switch __HOLE__ with input node
input: ast node, ast node with __HOLE__
output: ast node (with input node instead of __HOLE__)
'''
def fill_hole(input_node, holed_node):
  return switchNode(input_node).visit(holed_node)

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
