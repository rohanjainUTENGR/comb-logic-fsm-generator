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

if __name__ == "__main__":
    print("FSM Generator")
    input_file = "truth_table.txt"