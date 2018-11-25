import os

def convert_type(input):
    try:
      return int(input)
    except ValueError:
      try:
        return float(input)
      except ValueError:
        return input

def read_file(file_path):
  with open(file_path, 'r') as readfile:
    return readfile.read()

def get_fn_in_direc(direc):
  results = []
  for _, _, files in os.walk(direc):
    for f in files:
      results.append(f)
  return results

# Read input & output data
# directory (string) -> input data (number, string or array of them), output data (number, string or array of them)
def read_dataset(direc):
  input_direc = os.path.join(direc, 'input')
  output_direc = os.path.join(direc, 'output')
  fns = get_fn_in_direc(input_direc)
  
  input_data = []
  output_data = []
  for fn in fns:
    input_data.append(read_file(os.path.join(input_direc, fn)))
    output_data.append(read_file(os.path.join(output_direc, fn)))
  return input_data, output_data
# Test
# i, o = read_dataset('../testcase/max-dataset')
# print(i)
# print(o)

