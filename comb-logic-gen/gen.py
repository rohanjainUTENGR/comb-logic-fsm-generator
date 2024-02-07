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

def get_gate_max_inputs(op):
    if op == gate_operation.NAND:
        return 4
    if op == gate_operation.NOR:
        return 4
    if op == gate_operation.INV:
        return 1
    if op == gate_operation.AND:
        return 4
    if op == gate_operation.OR:
        return 4
    if op == gate_operation.XOR:
        return 2
    if op == gate_operation.XNOR:
        return 2

class wire:   
    def __init__(self, name):
        self.name = name
        self.input = input
        self.outputs = []
    
    def add_output(self, output):
        self.outputs.append(output)

    def add_input(self, input):
        self.input = input
    
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
        curr_num_inputs = len(self.inputs)
        op = self.operation
        self_max_inputs = get_gate_max_inputs(op)
        if (curr_num_inputs == self_max_inputs):
            print("Error: Max inputs for gate reached")
        else:
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
        if self.operation == gate_operation.AND:
            ret_val =  "and" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
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
            if len(exp_and) > 1:
                stack.append("AND")

            # print("stack: ")
            # print(stack)
            # print("\n-----------------------------------------------------------\n\n")
            stacks[output_label] = stack
            
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
    print("\n-----------------------------------------------------------\n\n")
    
    return reversed_stacks

def generate_verilog_module(dict, input_labels, output_labels):
    stack_wires = []

    for output in output_labels:
        print("expression: ")
        print(output)
        print("\n")
        gate_wire_dict = {}
        stack = dict[output]
        print("stack: ")
        print(stack)
        print('\n')
        while "NOT" in stack:
            while stack[-1] != 'NOT':
                print("\ninside NOT while loop")
                temp = stack.pop()
                print ("\nstack after pop: ")
                print (stack)
                print ('\n')
                if isinstance(temp, list) and len(temp) == 1:
                    temp = temp[0]            
                wire_not = wire("not_" + temp + "_wire")
                wire_not.add_input(temp)
                wire_name = wire_not.get_wire_name()

                gate_not = gate("not_" + temp, gate_operation.INV, wire_name)
                gate_not.add_input(temp)
                verilog_gate = gate_not.create_verilog_gate()

                gate_wire_dict[verilog_gate] = wire_name
                pprint.pprint(gate_wire_dict)
            print("ending pop: ")
            print(stack.pop())
            stack.append(wire_name)
               

        print ("\nstack at end of NOT: ")
        print (stack)

    
        while "AND" in stack:
            while (stack[-1] != "AND"):
                print("inside AND while loop")
                op1 = stack.pop()
                op2 = stack.pop()
                print ("\nstack after pop: ")
                print (stack)
                print ('\n')   
                if isinstance(op1, list) and len(temp) == 1:
                    op1 = op1[0]
                if isinstance(op2, list) and len(temp) == 1:
                    op2 = op2[0]
                wire_out = wire("and_" + op1 + "_" + op2 + "_wire")
                wire_out_name = wire_out.get_wire_name()

                gate_and = gate("and_" + op1 + "_" + op2, gate_operation.AND, wire_out_name)
                gate_and.add_input(op1)
                gate_and.add_input(op2)
                verilog_gate = gate_and.create_verilog_gate()
                print("verilog gate: ")
                print(verilog_gate)
                print("\n")

                gate_wire_dict[verilog_gate] = wire_out_name
                pprint.pprint(gate_wire_dict)
            print("ending pop: ")
            temp = stack.pop()
            print(temp)
            stack.append(wire_out_name)

        print("outside AND while loop")
        print(stack)
        print('\n-----------------------------------------------------\n')

if __name__ == "__main__":
    input_file = "truth_table.txt"
    
    min_truth_table = generate_minimized_truth_table(input_file)
    num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table = read_truth_table(min_truth_table)
    bool_expressions = generate_minimized_bool_expression(input_file)

    print ("\nbool expressions:")
    print(bool_expressions)
    print("\n")

    dict_bool_exp = read_min_bool_expression(bool_expressions, input_labels, output_labels)


    

    generate_verilog_module(dict_bool_exp, input_labels, output_labels)
