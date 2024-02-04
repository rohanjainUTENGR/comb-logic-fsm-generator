#!/bin/python3

# Rohan Jain
# ECE 382N19 Microarchitecture Spring 2024
# Generate a Verilog module using lib based on input truth table

import subprocess

def generate_minimized_truth_table(input_file):
    command = ['./../espresso.linux', 'truth_table.txt']
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing espresso.linux: {e}")

def read_truth_table(input):

    lines = input.split('\n')

    truth_table = []
    for line in lines[5:]:
        if line == '.e':
            break
        else:
            truth_table.append(line.split())
    print(truth_table)
    
if __name__ == "__main__":
    input_file = "truth_table.txt"
    min_truth_table = generate_minimized_truth_table(input_file)
    print(min_truth_table)
    read_truth_table(min_truth_table)
