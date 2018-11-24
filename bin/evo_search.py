import subprocess
import ast_manager
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
  for i in range(max_iteration):
    #mutate
    #seed_pool += mutation(seed_pool,mut_porb) - Tempo code.
    #seed_pool will be 150Gae
    seed_pool = lexicase_test([input_data, output_data], hole_tree, seed_pool, func_dict, runtime_limit)

    #left popul_size candidates. 0score candidates should be sorted randomly.
    seed_pool = seed_pool[:popul_size]
    if seed_pool[0].get_score()==1.0:
      #return should be fixed later.
      return seed_pool[0]
    if i%10==0:
      print('%dth iteration. max_score is %d'%(i,seed_pool[0].get_score()))

  '''if not succeed:
    return None
  return synth_code'''

def seeding(candidate, func_list, popul_size):
  #make seed 
  #By Hoon
  #used_cand_list is index list of be used for seeding pool in candidates. Make for refill mutation.
  #len(used_cand_list) should be same with popul_size
  return seed_pool, used_cand_list

def lexicase_test(test_case, hole_tree, seed_pool, func_dict, runtime_limit):
  #by Suk
  pool_size=len(seed_pool)
  scoring_start_index=0
  input_data, output_data = test_case
  test_num = len(input_data)

  for i in range(pool_size):
    if seed_pool[i].get_score()==None:#Assume that all none scoring seeds locate back.
      scoring_start_index=i
      break
  for i in range(scoring_start_index,pool_size):
    seed_pool[i].set_score(0.0)
  #If scoring_start_index is 0, all seeds should be scroing.

  for i in range(test_num):
    scoring_end_index_list=[]
    for j in range(scoring_start_index,pool_size):
      filled_code=ast_manager.fill_hole(hole_tree, seed_pool[j], func_dict)#will be changed after Sungho complete fill_hole function.
      with open('temp_test.py','w') as f:
        f.write(filled_code)
        f.close()
      try:
        #using python3 but with virtual env.
        result = subprocess.check_output ('python temp_test.py', input=input_data[i], 
        shell=True, timeout=runtime_limit, stderr=sys.STDERR, universal_newlines=True).strip()
        #Why strip?: result may have '\n' in end. so remove it. 
        if result == output_data[i]:
          seed_pool[j].set_score(seed_pool[j].get_score()+1.0)
        else:
          seed_pool[j].set_score(seed_pool[j].get_score()+0.5)
        if seed_pool[j].get_score==test_num: #All test case pass.
          seed_pool[j].set_score(1.0)
          seed_pool[0]=seed_pool[j]
          return seed_pool
      except Exception:
        scoring_end_index_list.append(j)
        #Time out, Runtime error, etc. Sanity check fail. scoring end.

    for j in scoring_end_index_list:
      if i > 1:
        seed_pool[j].set_score(seed_pool[j].get_score()/i)
      seed_pool[j], seed_pool[scoring_start_index] = seed_pool[scoring_start_index], seed_pool[j]
      scoring_start_index+=1

  for i in range(scoring_start_index, pool_size):
    seed_pool[i].set_score(seed_pool[i].get_score()/test_num)
  
  #Scoring end. Sorting.
  i=1
  while i < pool_size:
    tmp=seed_pool[i]
    j=i-1
    while seed_pool[j].get_score() < tmp.get_score() and j>-1:
      seed_pool[j+1]=seed_pool[j]
      j= j-1
    seed_pool[j+1]=tmp
    i+=1
  return seed_pool

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
    
