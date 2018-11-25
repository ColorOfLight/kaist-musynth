import subprocess
import ast_manager
import random
import sys
import astor
import ast
from mutations import \
  rebind_variable, fix_off_by_one, replace_variable_with_constant, delete_statement, insert_new_statement, refill
from logger import Logger

TEST_PATH = '../temp_test.py'

class codeCand(object):
  def __init__(self, node, source=None):
    self.node = node
    self.source = source
    self.score = None
  
  def set_score(self, score):
    self.score = score
  
  def set_node(self, node):
    self.node = node

  def get_score(self):
    return self.score
  
  def get_source(self):
    return self.source

  def get_node(self):
    return self.node

def run_evo(
  hole_tree, input_data, output_data, 
  cand_list, func_dict, hole_variable_list, hole_max_num,
  runtime_limit=0.5, max_iteration=1000,
  popul_size=100, mut_prob=[100, .1, .1, .1, .1, 100]):
  # input_data and output_data are string. How about candidates and draft_code?

  logger = Logger('test')

  seed_pool, used_cand_list = seeding(cand_list, popul_size)
  for i in range(max_iteration):
    #mutate
    seed_pool = mutate_cand_list(seed_pool, hole_variable_list, hole_max_num, mut_prob)

    #seed_pool will be 150Gae
    seed_pool = lexicase_test([input_data, output_data], hole_tree, seed_pool, func_dict, runtime_limit, logger)

    #left popul_size candidates. 0score candidates should be sorted randomly.
    seed_pool = seed_pool[:popul_size]

    if i % 1 == 0:
      print('%dth iteration. max_score is %.2f' %
            (i+1, seed_pool[0].get_score()))

    if seed_pool[0].get_score()==1.0:
      #return should be fixed later.
      return seed_pool[0]

  '''if not succeed:
    return None
  return synth_code'''

# Hoon
# Input : candidate - list of codeCand, pop_size - size of population
# Output : seed_pool - randomly seleted codeCand, used_cand_list - list of indices selected
def seeding(candidates, pop_size):

  if len(candidates) >= pop_size:
    used_cand_list = random.sample(range(len(candidates)), pop_size)
    seed_pool = [candidates[i] for i in used_cand_list]
  else:
    used_cand_list = list(range(len(candidates)))
    seed_pool = candidates

  # assert(len(used_cand_list) == pop_size)

  return seed_pool, used_cand_list

def lexicase_test(test_case, hole_tree, seed_pool, func_dict, runtime_limit, logger):
  #by Suk
  pool_size=len(seed_pool)
  input_data, output_data = test_case
  test_num = len(input_data)

  None_scoring_list=[]
  for i in range(pool_size):
    if seed_pool[i].get_score()==None:
      None_scoring_list.append(i)
      seed_pool[i].set_score(0.0)
  #If scoring_start_index is 0, all seeds should be scroing.

  for i in range(test_num):
    scoring_end_list=[]
    for j in None_scoring_list:
      logger.log(astor.to_source(seed_pool[j].get_node()))
      filled_code=ast_manager.fill_hole(seed_pool[j], hole_tree, func_dict)#will be changed after Sungho complete fill_hole function.
      with open(TEST_PATH, 'w') as f:
        f.write(filled_code)
      try:
        #using python3 but with virtual env.
        result = subprocess.check_output(f'python {TEST_PATH}', input=input_data[i],
        shell=True, timeout=runtime_limit, stderr=subprocess.STDERR, universal_newlines=True).strip()
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
        scoring_end_list.append(j)
        None_scoring_list.remove(j)
        #Time out, Runtime error, etc. Sanity check fail. scoring end.

    for j in scoring_end_list:
      if i > 1:
        seed_pool[j].set_score(seed_pool[j].get_score()/i)

  for i in None_scoring_list:
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
    i=i+1
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
    
'''
mutate_cand_list
input: list of codeCand
output: list of codeCand (mutated cands are added)
'''
def mutate_cand_list(cand_list, hole_variable_list, hole_max_num, mut_prob):
  mutated_cand_list = []
  index_list = list(range(6))
  
  for cand in cand_list:
    shuffled_indexes = _weigthed_shuffle(index_list, mut_prob)
    for i in shuffled_indexes:
      if i == 0:
        new_cand = rebind_variable(cand, hole_variable_list)
      elif i == 1:
        new_cand = fix_off_by_one(cand)
      elif i == 2:
        new_cand = replace_variable_with_constant(cand, hole_max_num)
      elif i == 3:
        new_cand = delete_statement(cand)
      elif i == 4:
        new_cand = insert_new_statement(cand, cand_list)
      elif i == 5:
        new_cand = refill(cand, cand_list)
      else:
        new_cand = None
      
      if new_cand != None:
        mutated_cand_list.append(new_cand)
        break

  return cand_list + mutated_cand_list

def _weigthed_shuffle(items, weights):
    order = sorted(range(len(items)), key=lambda i: -
                   random.random() ** (1.0 / weights[i]))
    return [items[i] for i in order]
