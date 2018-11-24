import subprocess
import sys

class codeCand(Object):
  def __init__(self, node, source):
    self.node = node
    self.source = source
    self.score = None
  
  def set_score(self, score):
    self.score = score

  def get_score(self):
    return self.score
  
  def get_source(self):
    return self.source

def run_evo(
  hole_tree, input_data, output_data, 
  cand_list, func_list, hole_variable_list, hole_max_num,
  runtime_limit=0.5, max_iteration=1000,
  popul_size=100, mut_prob=[.5, .5, .5, .5, .5, .5]):
#input_data and output_data are string. How about candidates and draft_code?

  seed_pool,used_cand_list = seeding(cand_list, func_list, popul_size)
  max_score=0.0
  for i in range(max_iteration):
    #mutate
    #seed_pool = mutation(seed_pool,mut_porb) - Tempo code.
    #seed_pool will be 150Gae
    max_score, seed_pool = lexicase_test([input_data, output_data], seed_pool, runtime_limit)

    #left popul_size candidates. 0score candidates should be sorted randomly.
    seed_pool = seed_pool[:popul_size]
    if max_score==1.0:
      #return should be fixed later.
      return seed_pool[0]
    if i%10==0:
      print('%dth iteration. max_score is %d'%(i,max_score))

  '''if not succeed:
    return None
  return synth_code'''

def seeding(candidate, func_list, popul_size):
  #make seed 
  #By Hoon
  #used_cand_list is index list of be used for seeding pool in candidates. Make for refill mutation.
  #len(used_cand_list) should be same with popul_size
  return seed_pool, used_cand_list

def lexicase_test(test_case, hole_tree, seed_list, runtime_limit)
  #by Suk
  test_num = len(test_case)
  for i in range(test_num):
    break

  return max_score, seed_list


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
    
