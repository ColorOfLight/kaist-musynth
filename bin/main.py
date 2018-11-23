# from evo_search import run_evo
# from read import get_draft_code, get_candidates
from ast_manager import fill_hole
import astor
import ast

# >> python bin/main.py draft_fn test_direc
draft_fn = '../sample.py'
output_fn = '../output.py'

# Get Input code 
# draft_code = get_draft_code(draft_fn)
hole_tree = astor.code_to_ast.parse_file(draft_fn)

input_node = ast.Import(names=[ast.alias(name='quux', asname=None)])
hole_tree = fill_hole(input_node, hole_tree)

with open(output_fn, 'w') as writefile:
  writefile.write(astor.to_source(hole_tree))

'''
# Get dataset
input_data, output_data = read_dataset(test_direc)

# Read hole and get Candidates
# hole_comment: sort /// A
candidates = get_candidates(hole_comment)

# If it fails, return null
synth_code = run_evo(draft_code, input_data, output_data, candidates)

if synth_code:
  # write_new_file
  print("Success")
'''
