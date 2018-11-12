from evo_search import run_evo
from read import get_draft_code, get_candidates, read_dataset

# >> python bin/main.py draft_fn test_direc

# Get Input code 
draft_code, hole_comment = get_draft_code(draft_fn)

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
