import subprocess
import sys
def run_evo(
  hole_tree, input_data, output_data, input_data, output_data,
  runtime_limit=500, max_iteration=1000,
  popul_size=50, mut_prob=[.5, .5, .5, .5, .5, .5]):
#input_data and output_data are string. How about candidates and draft_code?
  if not succeed:
    return None
  return synth_code

def seeding(candidate, popul_size):
  return seed_pool
#make seed 

def fitness(draft_code, runtime_limit, input_data, output_data):
#input_data and output_data is string. just read from file.
'''
example of outputdata

with open('output_1.txt') as f:
	output_data=f.read()
	f.close()
'''
#draft_code should be code whose hole is fulled with candidate. Not AST!!
  #score will be 0.0 ~ 1.0. If score is 1.0, it will ends. perfect!  
  
  #save draft code as temp_test.py
  with open('temp_test.py','w') as f:
    f.write(draft_code)
    f.close()

  test_num = len(input_data)
  test_score = 0.0
  for i in range(test_num):
    try:
      #using python3 but with virtual env.
      result = subprocess.check_output ('python temp_test.py', input=input_data[i] , 
      shell=True, timeout=runtime_limit, stderr=sys.STDERR,universal_newlines=True).strip()
     #strip: result may have '\n' in end. so remove it. 
    except subprocess.TimeoutExpired:
      #Time limit error. Let's check next case.g
      continue
    except Exception:
      #Rest errors. Number error, Runtime error, etc. Sanity check fail. score is 0.
      return 0.0
    if result == output_data[i]:
      test_score += 1.0
    else:
      test_score += 0.5
    #if output is right, plus 1/n point and if output  coume out but is wrong, plus 0.5/n point
  return test_score / test_num
    
