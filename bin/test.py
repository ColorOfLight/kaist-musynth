import astor
import ast
from ast_manager import generate_candidates, add_suffix_to_funcdef

# class v(ast.NodeVisitor):
#   def __init__(self):
#     self.level = 0

#   def generic_visit(self, node):
#     print(astor.to_source(node))
#     self.level += 1
#     ast.NodeVisitor.generic_visit(self, node)

# pool_name = 'sample1'
# tree = astor.code_to_ast.parse_file('../sample.py')
# nodes = ast.walk(tree)
# func_nodes = []
# for node in nodes:
#   # print(node)
#   if isinstance(node, ast.FunctionDef):
#     func_nodes.append(node)
#     node.name = 'test'
#     print(astor.to_source(node))

# path = '../code-pool/sort'
# cand_dict, func_dict = generate_candidates(path)

# print(cand_dict)

# visitor = v()
# visitor.visit(tree)

# code = astor.to_source(tree)
# print(code)

# Module, Assign, For, Expr, Name, List, Call, Num, Load, Store, BinOp, If, Sub, Compare, Subscript, Index
# Assign, For, Call(?), If, While, FunctionDef
hole_tree = astor.code_to_ast.parse_file('../sample.py')
# print(ast.dump(hole_tree))
new_tree = add_suffix_to_funcdef(hole_tree, '_test')
print(astor.to_source(new_tree))
