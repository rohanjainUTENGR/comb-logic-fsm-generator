#!/bin/python3

# Rohan Jain
# ECE 382N19 Microarchitecture Spring 2024
# Generate an optimaized Verilog module using lib based on input truth table

import subprocess
from enum import Enum

class gate_operation(Enum):
    NAND = 1 # max 4 inputs
    NOR = 2 #  max 4 inputs
    INV = 3 # NOT- max 1 input
    AND = 4 # max 4 inputs
    OR = 5  # max 4 inputs
    XOR = 6 # max 2 inputs
    XNOR = 7 # max 2 inputs

class wire:   
    def __init__(self, name, input):
        self.name = name
        self.input = input
        self.outputs = []
    
    def add_output(self, output):
        self.outputs.append(output)

class gate:
    def __init__(self, name, operation, output_wire):
        self.name = name
        self.operation = operation
        self.inputs = []
        self.output = output_wire
    
    def add_input(self, input):
        self.inputs.append(input)

    def create_verilog_gate(self):
        if self.operation == gate_operation.NAND:
            ret_val =  "nand" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
            print(ret_val)
            return ret_val    

def generate_minimized_truth_table(input_file):
    command = ['./../espresso.linux', 'truth_table.txt']
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing espresso.linux: {e}")

def generate_minimized_bool_expression(input_file):
    command = ['./../espresso.linux', '-o', 'eqntott', 'truth_table.txt']
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing espresso.linux -o eqntott: {e}")

def read_truth_table(input):
    lines = input.split('\n')
    num_inputs = int(lines[0].split()[1])
    num_outputs = int(lines[1].split()[1])
    input_labels = lines[2].split()[1:]
    output_labels = lines[3].split()[1:]
    num_rows = int(lines[4].split()[1])

    truth_table = []
    for line in lines[5:]:
        if line == '.e':
            break
        else:
            truth_table.append(line.split())
    # print(truth_table)
    print(num_inputs, num_outputs, input_labels, output_labels, num_rows)
    return num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table

def read_min_bool_expression(bool_exps, input_labels, output_labels):
    lines = bool_exps.split('\n')
    for line in lines:
        if line == '':
            continue
        else:
            # make a tree with parent as OR and children as AND and leaf as input

            curr_exp = line.split('=')
            input_label = curr_exp[0]
            exp = curr_exp[1]
            exp = exp[2:-2] #remove starting and ending parenthesis and ending semicolon

            exp.strip('|')
            #num_terms_or = exp.len
            # first layer of tree is of length num_terms_or

            # print("split based on OR: ")
            # print(exp)
            
            # print("\n")

            # exp = exp.split('&')
            # print("split based on AND: ")
            # print(exp)
            # print("\n")

            # # for each term in exp, split based on NOT
            # for term in exp:
            #     exp_not = term.split('!')
            #     print("split based on NOT: ")
            #     print(exp_not)
            #     print("\n")



if __name__ == "__main__":
    input_file = "truth_table.txt"
    min_truth_table = generate_minimized_truth_table(input_file)
    num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table = read_truth_table(min_truth_table)
    bool_expressions = generate_minimized_bool_expression(input_file)
    print(bool_expressions)
    print("\n")
    read_min_bool_expression(bool_expressions, input_labels, output_labels)


    test_gate = gate("test_gate", gate_operation.NAND, "out")
    test_gate.add_input("in1")
    test_gate.add_input("in2")
    test_gate.create_verilog_gate()
    