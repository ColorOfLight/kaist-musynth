# from evo_search import run_evo
# from read import get_draft_code, get_candidates
from ast_manager import fill_hole, generate_candidates, get_name_list, get_max_val
from read import read_dataset
from evo_search import run_evo
import astor
import ast
import os

# >> python bin/main.py draft_fn test_direc
test_name = 'insertion-sort'


# Get Input code 
hole_tree = astor.code_to_ast.parse_file(os.path.join('../testcase', test_name + '.py'))
hole_variable_list = get_name_list(hole_tree)
hole_max_num = get_max_val(hole_tree)

# Get dataset
input_data, output_data = read_dataset(os.path.join('../testcase', test_name+'-dataset'))

# Read hole and get Candidates
# hole_comment: sort /// A
cand_list, func_dict = generate_candidates(os.path.join('../code-pool'))

# If it fails, return null
r, nr = [], []
for i in range(5):
  synth_code, iteration = run_evo(
    hole_tree, input_data, output_data, cand_list, func_dict,
    hole_variable_list, hole_max_num, is_random=True)
  if synth_code:
    print(f"Random-none: {i} - {iteration} iterations")
    r.append(iteration)

for i in range(5):
  synth_code, iteration = run_evo(
    hole_tree, input_data, output_data, cand_list, func_dict,
    hole_variable_list, hole_max_num, is_random=False)
  if synth_code:
    print(f"Evo-none: {i} - {iteration} iterations")
    nr.append(iteration)

print(f"Random-none: {sum(r) / 5}, Evo-none: {sum(nr) / 5}")
