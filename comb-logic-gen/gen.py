#!/bin/python3

# Rohan Jain
# ECE 382N19 Microarchitecture Spring 2024
# Generate an optimaized Verilog module using lib based on input truth table

import subprocess

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
            # remove starting and ending parenthesis and ending semicolon
            curr_exp = line.split('=')
            input_label = curr_exp[0]
            exp = curr_exp[1]
            exp = exp[2:-2] #remove starting and ending parenthesis and ending semicolon

            exp.strip('|')
            print("split based on OR: ")
            print(exp)
            print("\n")

            exp = exp.split('&')
            print("split based on AND: ")
            print(exp)
            print("\n")




if __name__ == "__main__":
    input_file = "truth_table.txt"
    min_truth_table = generate_minimized_truth_table(input_file)
    num_inputs, num_outputs, input_labels, output_labels, num_rows, truth_table = read_truth_table(min_truth_table)
    bool_expressions = generate_minimized_bool_expression(input_file)
    print(bool_expressions)
    print("\n")
    read_min_bool_expression(bool_expressions, input_labels, output_labels)
    