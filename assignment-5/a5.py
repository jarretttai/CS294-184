from z3 import *
import sys

def is_obstacle(pos_x, pos_y, obs):
	return Or([And(pos_x == obs[i][0], pos_y == obs[i][1]) for i in range(len(obs))])

def run_instr_x(pos_x, pos_y, instr, envir, obs):

	return  If(instr == 0, 
				If(pos_x - 1 >= 0, 
					If(is_obstacle(pos_x - 1, pos_y, obs), pos_x, pos_x - 1), 
				pos_x), 
			If(instr == 1, 
				If(pos_x + 1 < envir, 
					If(is_obstacle(pos_x + 1, pos_y, obs), pos_x, pos_x + 1),  
				pos_x)
			, pos_x))


def run_instr_y(pos_x, pos_y, instr, envir, obs):

	return 	If(instr == 2, 
				If(pos_y - 1 >= 0, 
					If(is_obstacle(pos_x, pos_y - 1, obs), pos_y, pos_y - 1), 
				pos_y), 
			If(instr == 3, 
				If(pos_y + 1 < envir, 
					If(is_obstacle(pos_x, pos_y + 1, obs), pos_y, pos_y + 1), 
				pos_y)
			, pos_y))


def run_prog_y(pos_x, pos_y, instrs, envir, obs):
	curr_pos_x = pos_x
	curr_pos_y = pos_y
	for i in range(len(instrs)):
		curr_pos_x = run_instr_x(curr_pos_x, curr_pos_y, instrs[i], envir, obs)
		curr_pos_y = run_instr_y(curr_pos_x, curr_pos_y, instrs[i], envir, obs)
	return curr_pos_y


def run_prog_x(pos_x, pos_y, instrs, envir, obs):
	curr_pos_x = pos_x
	curr_pos_y = pos_y
	for i in range(len(instrs)):
		curr_pos_x = run_instr_x(curr_pos_x, curr_pos_y, instrs[i], envir, obs)
		curr_pos_y = run_instr_y(curr_pos_x, curr_pos_y, instrs[i], envir, obs)
	return curr_pos_x


# left: 0x00, right: 0x01, up: 0x10, down: 0x11, stay: 0x100 - 0x111
def gen_instrs(num_instrs):
	return [BitVec('x_'+str(i),3) for i in range(num_instrs)]


# a convenience function for printing the Z3 output to look like a sequence of instructions
def print_model(model, instrs):
	for i in range(len(instrs)):
		val = model.eval(instrs[i])
		if val == 0:
			print("L")
		elif val == 1:
			print("R")
		elif val == 2:
			print("U")
		elif val == 3:
			print("D")
		else:
			print("-")


# The default value is 4
num_instrs = int(sys.argv[1]) if len(sys.argv) > 1 else 4

for i in range(num_instrs + 1):
	instrs = gen_instrs(i) # generate BVs to represent instructions

	# obstacles
	obs = [[9, 5]]
	# impossible obstacles
	# obs = [[8, 4], [9, 3], [10, 4], [9, 5]]

	# src: (8, 6)
	# dst: (9, 4)
	goal = And(run_prog_x(8, 6, instrs, 16, obs) == 9, run_prog_y(8, 6, instrs, 16, obs) == 4) # where do we want our robot to move?

	s = Solver()
	s.add(goal)
	satisfiable = s.check()
	print("\nlength of %d satisfiable? %s" % (i, satisfiable))
	if (satisfiable == sat):
		model = s.model()
		print_model(model, instrs) # print the program if we found one
		print(model) # print the model, just to visualize what's happening underneath

	