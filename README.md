# CS454 Team \#7 - Kaisynth

Program Synthesis via Code Reuse and Code Manipulation for Python

## Running Environments

## Design

### Input
- Program with a code hole defined by us
- One part of program was subtituted by HOLE (ex. __HOLE__ = None)
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
> Let's say that the hole code is A, and the donated code snippet is B.

- Rebind Variables
  - Change the name of variable in B to the name in A.
- Fix off-by-one
  - Decrease the value of constant in B by one.
- Replace variable with a constant
  - Change the variable in B into new constant value.
- Delete statement
  - If B consists of more than one line, delete one line from B.
- Insert new statement (insert a new donor statement at random within the hole)
  - Insert a new line into B regarding surrounding context of B

## Reference

- [Kashyap, Vineeth, et al. "MuSynth: Program Synthesis via Code Reuse and Code Manipulation." International Symposium on Search Based Software Engineering. Springer, Cham, 2017.](https://www.cs.unm.edu/~eschulte/data/musynth-ssbse-2017.pdf)

## Note
[Coding Note](https://docs.google.com/document/d/1hLi2X2IPnlgibq43QuFGgWyoxq_AYgm_SaxbF97RMJI/edit?usp=sharing)
