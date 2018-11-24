# from evo_search import run_evo
# from read import get_draft_code, get_candidates
from ast_manager import fill_hole, generate_candidates
from read import read_dataset
from evo_search import run_evo
import astor
import ast
import os

# >> python bin/main.py draft_fn test_direc
test_name = 'insertion-sort'


# Get Input code 
hole_tree = astor.code_to_ast.parse_file(os.path.join('../testcase', test_name + '.py'))

# Get dataset
input_data, output_data = read_dataset(os.path.join('../code-pool', test_name))

# Read hole and get Candidates
# hole_comment: sort /// A
cand_dict, func_dict = generate_candidates(os.path.join('../code-pool', test_name))


# If it fails, return null
synth_code = run_evo(hole_tree, input_data, output_data, input_data, output_data)
'''
if synth_code:
  # write_new_file
  print("Success")
'''
