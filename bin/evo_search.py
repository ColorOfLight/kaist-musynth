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
    self.avg_score = 0.0
  
  def init_score(self):
    self.score = 0

  def set_score(self, score):
    self.score = score

  def add_score(self, score):
    if self.score == None:
      self.score = score
    else:
      self.score += score
  
  def get_score(self):
    return self.score
  
  def set_avg_score(self, case_num):
    if self.score != None:
      self.avg_score = self.score/case_num

  def get_avg_score(self):
    return self.avg_score

  def set_node(self, node):
    self.node = node
  
  def get_source(self):
    return self.source

  def get_node(self):
    return self.node

def run_evo(
  hole_tree, input_data, output_data, 
  cand_list, func_dict, hole_variable_list, hole_max_num,
  runtime_limit=0.5, max_iteration=1000,
  popul_size=200, mut_prob=[3, 1, 1, 3, 0.0001, 0.0001]):
  # input_data and output_data are string. How about candidates and draft_code?

  logger = Logger('test')

  seed_pool, _ = seeding(cand_list, popul_size)
  for i in range(max_iteration):
    #mutate
    seed_pool = mutate_cand_list(seed_pool, hole_variable_list, hole_max_num, mut_prob)

    #seed_pool will be 150Gae
    seed_pool = lexicase_test(seed_pool, hole_tree, func_dict, input_data, output_data, runtime_limit, logger)

    #left popul_size candidates. 0score candidates should be sorted randomly.
    seed_pool = seed_pool[:popul_size]

    print('%dth iteration. max_score is %.2f' %
          (i+1, seed_pool[0].get_avg_score()))

    if seed_pool[0].get_avg_score()==1.0:
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


def lexicase_test(seed_pool, hole_tree, func_dict, input_data, output_data, runtime_limit, logger):
  pool_size = len(seed_pool)
  test_num = len(input_data)

  answer_found = False
  for cand_code in seed_pool:
    # If score is already calculated, skip this step.
    if cand_code.get_score() != None:
      continue
    if answer_found:
      break

    filled_code=ast_manager.fill_hole(cand_code, hole_tree, func_dict)
  
    assert(len(input_data) == len(output_data))
    case_num = len(input_data)

    for i in range(case_num):
      input_value = input_data[i]
      output_value = output_data[i]

      with open(TEST_PATH, 'w') as f:
        f.write(filled_code)
      try:
        # run code with python3 in virutalenv.
        result = subprocess.check_output(f'python {TEST_PATH}', input=input_value,
        shell=True, timeout=runtime_limit, stderr=subprocess.STDOUT, universal_newlines=True).strip()

        if result == output_value:
          cand_code.add_score(1.0)
        else:
          cand_code.add_score(0.5)

        # cand_code is the answer.
        if cand_code.get_score() == test_num:
          answer_found = True
          break


      except Exception:
        # This step should be finished if sanity check failed. (e.g. runtime error, timeout, etc.)
        if cand_code.get_score() == None:
          cand_code.init_score()
        break

    cand_code.set_avg_score(case_num)

    logger.log(astor.to_source(cand_code.get_node()))
    logger.log(cand_code.get_avg_score())

  sorted_pool = sorted(seed_pool, key=lambda x: x.avg_score, reverse=True)
  return sorted_pool

  

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
        new_cand = refill(cand, cand_list, hole_variable_list)
      elif i == 4:
        new_cand = delete_statement(cand)
      elif i == 5:
        new_cand = insert_new_statement(cand, cand_list)
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
