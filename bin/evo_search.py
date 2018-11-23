import subprocess
import time

def run_evo(
  draft_code, input_data, output_data, candidates
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
#draft_code should be code whose hole is fulled with candidate. Not AST!!
  #score will be 0.0 ~ 1.0. If score is 1.0, it will ends. perfect!  
  
  with f=open('test.py','w'):
    f.write(draft_code)
    f.close()

  test_num = len(input_data)
  test_score = 0.0
  for i in range(test_num):
    try:
      result = subprocess.check_output ('python test.py '+input_data[i] , 
      shell=True, timeout=runtime_limit, stderr=STDERR,universal_newlines=True).strip()
     #strip: result may have '\n' in end. so remove it. 
    except subprocess.TimeoutExpired:
      continue
    except Exception:
      return 0.0
    if result == output_data[i]:
      test_score += 1.0
  return test_score / test_num
    