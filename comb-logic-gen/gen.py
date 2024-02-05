#!/bin/python3

# Rohan Jain
# ECE 382N19 Microarchitecture Spring 2024
# Generate an optimaized Verilog module using lib based on input truth table

import subprocess
import pprint
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
    
    def create_verilog_wire(self):
        return "wire " + self.name + ";"
    
    def get_wire_name(self):
        return self.name

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
            #print(ret_val)
            return ret_val
        if self.operation == gate_operation.INV:
            ret_val =  "inv" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
            #print(ret_val)
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
    stacks = {}
    for line in lines:
        if line == '':
            continue
        else:
            stack = []
            curr_exp = line.split('=')
            output_label = curr_exp[0]
            output_label = output_label.strip()
            exp = curr_exp[1]
            exp = exp[2:-2] #remove starting and ending parenthesis and ending semicolon
            # print("current expression: ")
            # print(exp)
            # print("\n")

            exp_or = exp.strip('|')
            num_terms_or = len(exp_or)

            # print("split based on OR: ")
            # print(exp_or)
            # print("\n")

            exp_and = exp_or.split('&')
            exp_and = list(filter(None, exp_and))
            # print("split based on AND: ")
            # print(exp_and)
            # print("\n")

            for term in exp_and:
                if term[0] == '!':
                    exp_not = term.split('!')
                    exp_not = list(filter(None, exp_not))
                    # print("split based on NOT: ")
                    # print(exp_not)
                    # print("\n")
                    stack.append(exp_not)
                    stack.append("NOT")
            for term in exp_and:
                if term[0] != '!':
                    stack.append(term)
            # print("stack after AND: ")
            # print(stack)
            # print("\n")
            if len(stack) == 1:
                stacks[output_label] = stack
                continue
            stack.append("AND")

            # print("stack: ")
            # print(stack)

            stacks[output_label] = stack
            # print("\n-----------------------------------------------------------\n\n")
    print("\n")
    print("Stacks dictionary: ")
    pprint.pprint(stacks)
    print("\n")           

    reversed_stacks = {}
    for output in output_labels:
        stack = stacks[output]
        reversed_stacks[output] = list(reversed(stack))

    print("\n")
    print("Reversed Stacks dictionary: ")
    pprint.pprint(reversed_stacks)
    print("\n")

    return reversed_stacks

def generate_verilog_module(dict, input_labels, output_labels):
    for output in output_labels:
        gate_wire_dict = {}
        stack = dict[output]
        print("stack: ")
        print(stack)
        print('\n')
        if "NOT" in stack:
            while stack[-1] != 'NOT':
                print("inside NOT while loop")
                temp = stack.pop()
                if temp == 'NOT':
                    #why is this detection not working properly?
                    print("popped NOT")
                    continue
                print ("\nstack after pop: ")
                print (stack)
                if isinstance(temp, list) and len(temp) == 1:
                    temp = temp[0]            
                wire_not = wire("not_" + temp + "_wire", temp)
                wire_name = wire_not.get_wire_name()

                gate_not = gate("not_" + temp, gate_operation.INV, wire_name)
                gate_not.add_input(temp)
                verilog_gate = gate_not.create_verilog_gate()

                gate_wire_dict[verilog_gate] = wire_name
                pprint.pprint(gate_wire_dict)
                
                

        print ("\nstack at end of NOT: ")
        print (stack)

    
        if "AND" in stack:
            while stack[-1] != "AND":
                print("inside AND while loop")
                print(stack.pop())
                print('\n')

        print("outside while loop")
        print(stack)
        print('\n-----------------------------------------------------\n')

         




if __name__ == "__main__":
    input_file = "truth_table.txt"
    min_truth_table = generate_minimized_truth_table(input_file)
    num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table = read_truth_table(min_truth_table)
    bool_expressions = generate_minimized_bool_expression(input_file)
    print(bool_expressions)

    dict_bool_exp = read_min_bool_expression(bool_expressions, input_labels, output_labels)
    generate_verilog_module(dict_bool_exp, input_labels, output_labels)
