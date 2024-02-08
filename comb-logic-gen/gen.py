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
        elif self.operation == gate_operation.INV:
            ret_val =  "inv" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
            #print(ret_val)
            return ret_val
        elif self.operation == gate_operation.AND:
            ret_val =  "and" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
            #print(ret_val)
            return ret_val   
        elif self.operation == gate_operation.OR:
            ret_val =  "or" + str(len(self.inputs)) + "$ " + self.name + " (" + self.output  + ", " + ", ".join(self.inputs) + ");"
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

def generate_verilog_statements(dict, input_labels, output_labels, output_file):

    gate_wire_dict = {}
    wire_output_dict = {}

    for output in output_labels:
        print("expression: ")
        print(output)
        print("\n")
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
                wire_not = wire(output + "_" + "not_" + temp + "_wire")
                wire_not.add_input(temp)
                wire_name = wire_not.get_wire_name()

                gate_not = gate(output + "_" + "not_" + temp, gate_operation.INV, wire_name)
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
                wire_out = wire(output + "_" + "and_" + op1 + "_" + op2 + "_wire")
                wire_out_name = wire_out.get_wire_name()

                gate_and = gate(output + "_" + "and_" + op1 + "_" + op2, gate_operation.AND, wire_out_name)
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

        while 'OR' in stack:
            while (stack[-1] != 'OR'):
                print("inside OR while loop")
                op1 = stack.pop()
                op2 = stack.pop()
                print ("\nstack after pop: ")
                print (stack)
                print ('\n')   
                if isinstance(op1, list) and len(op1) == 1:
                    op1 = op1[0]
                if isinstance(op2, list) and len(op2) == 1:
                    op2 = op2[0]
                wire_out = wire(output + "_" + "or_" + op1 + "_" + op2 + "_wire")
                wire_out_name = wire_out.get_wire_name()

                gate_or = gate(output + "_" + "or_" + op1 + "_" + op2, gate_operation.OR, wire_out_name)
                gate_or.add_input(op1)
                gate_or.add_input(op2)
                verilog_gate = gate_or.create_verilog_gate()
                print("verilog gate: ")
                print(verilog_gate)
                print("\n")

                gate_wire_dict[verilog_gate] = wire_out_name
                pprint.pprint(gate_wire_dict)
        print("outside OR while loop")
        print(stack)

        pprint.pprint(gate_wire_dict)
        #get a subset of the gate_wire_dict that has the the output name as a part of the key
        for output in output_labels:
            temp = []
            outputlen = len(output)
            #print("outputlen: " + str(outputlen))
            for key in gate_wire_dict:
                val = gate_wire_dict[key]
                substr = val[0:outputlen]
                print("substr: " + substr + "\n")
                if output in substr:
                    temp.append(val)
                    print("temp: ")
                    pprint.pprint(temp)
                    print("\n")
            if temp != []:
                wire_output_dict[output] = max(temp, key=len)
        print("\n")
        pprint.pprint(wire_output_dict)

        for output in output_labels:
            print(output)
            if output not in wire_output_dict:
                temp = dict[output]
                if isinstance(temp, list) and len(temp) == 1:
                    temp = temp[0]
                wire_output_dict[output] = temp
                
                
        print('\n-----------------------------------------------------\n')
    return gate_wire_dict, wire_output_dict

def generate_verilog_module(output_file, output_labels, input_labels, gate_wire_dict, wire_output_dict):    
    output_file.write("module comb_logic (")

    for label in range(len(input_labels)):
        if label != 0:
            output_file.write("\t")
        output_file.write("input " + input_labels[label] + ",\n")
    for label in range(len(output_labels)):
        output_file.write("\toutput " + output_labels[label])
        if label != len(output_labels) - 1:
            output_file.write(",\n")
    output_file.write(");\n\n")

    for wire in gate_wire_dict.values():
        output_file.write("\twire " + wire + ";\n")
    
    output_file.write("\n")

    for gate in gate_wire_dict:
        output_file.write("\t" + gate + "\n")

    output_file.write("\n")

    for output in output_labels:
        output_file.write("\tassign " + output + " = " + wire_output_dict[output] + ";\n")

    output_file.write("\nendmodule")

if __name__ == "__main__":
    input_file = "truth_table.txt"
    output_file = open("module.v", "w")
    
    min_truth_table = generate_minimized_truth_table(input_file)
    num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table = read_truth_table(min_truth_table)
    bool_expressions = generate_minimized_bool_expression(input_file)

    print ("\nbool expressions:")
    print(bool_expressions)
    print("\n")

    dict_bool_exp = read_min_bool_expression(bool_expressions, input_labels, output_labels)

    gate_wire_dict, wire_output_dict = generate_verilog_statements(dict_bool_exp, input_labels, output_labels, output_file)

    generate_verilog_module(output_file, output_labels, input_labels, gate_wire_dict, wire_output_dict)
    