Rohan Jain

ECE 382N19 - Microarchitecture (graduate) with Dr. Yale Patt

Spring 2024

The University of Texas at Austin

Developed with help from [Espresso tool](https://ptolemy.berkeley.edu/projects/embedded/pubs/downloads/espresso/index.htm) developed by UC Berkeley. 
Generated Verilog modules use gates from UT Austin ECE Microarchitecture lib.

## comb-logic-gen
Generate a Verilog module from a truth table using modules from lib. 
The inputted truth table will have the following format and should be named truth_table.txt
````
.i 2
.o 4
.ilb in[1] in[0] 
.ob out[0] out[1] out[2] out[3] 

00 1000
01 0100
10 0010
11 0001
````
.i - number of inputs

.o - number of outputs

.ilb - labels for inputs

.ob - labels for outputs

## fsm-logic-gen
Generate a Moore FSM Verilog module based on inputted truth table. The truth table should also be called truth_table.txt and have the same format as above.

