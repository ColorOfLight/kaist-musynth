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
Add suffix to names of funcs
input: string of code
output: string of code
'''
# def add_suffix_to_funcs()
