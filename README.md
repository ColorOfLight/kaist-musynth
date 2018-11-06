# CS454 Team \#7 - Musynth

Program Synthesis via Code Resue and Code Manipulation for Python

## Design

### Input
- Program with a code hole defined by us
- Hole is line of comment (ends with ```HOLE```)
- An explanation for the hole written in the comment
```
>> max.py

# INPUT: [5 7 3]
# OUTPUT: 7

A = array_from_args()
# HOLE: sort /// A
print(A[-1])
```

### Code Pool

- Manually generated code for algorithm (search, sort and etc)
- Copy code snippets from the Internet (StackOverflow ... )

### Evolutionary Search

#### Seeding
Get candidates from code pool
- Ideal: match the hole explanation & explanation of code from the pool
- Real: get candidates from certain directory

#### Evaluate
- Fitness function
  - Sanity check
    - Error (1/0)
    - Runtime (~500ms : 1 / 0)
  - Developer check
    - Match input & output (percentage of passed cases)

Parameters

| Param Name       | Default          | 
| ------------- |-------------| 
| Runtime limit     | 500ms |
| Iteration | 1000 |
| Population size  | 50 |
| Mutation Prob. | .5 (all) |
> Mutation Probability is list of probabilities in order specified below

#### Selection (can be changed)
- lexicase selection
- tournament selection

#### Mutation
- Rebind (change variable name from )
- Fix off-by-one (change constant name)
- Replace variable with a constant
- Delete statement
- Refill (which throws away the current contents of the hole and refills with new donor snippet)
- insert new statement (insert a new donor statement at random within the hole)

## Reference

## Note
[Coding Note](https://docs.google.com/document/d/1hLi2X2IPnlgibq43QuFGgWyoxq_AYgm_SaxbF97RMJI/edit?usp=sharing)