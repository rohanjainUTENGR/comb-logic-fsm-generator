module comb_logic (input clk, 
	input in[1],
	input in[0],
	output out[0],
	output out[1],
	output out[2],
	output out[3]);

	wire out[0]_not_in[1]_wire;
	wire out[2]_not_in[0]_wire;
	wire out[2]_and_out[2]_not_in[0]_wire_in[1]_wire;
	wire out[3]_and_in[1]_in[0]_wire;

	inv1$ out[0]_not_in[1] (out[0]_not_in[1]_wire, in[1]);
	inv1$ out[2]_not_in[0] (out[2]_not_in[0]_wire, in[0]);
	and2$ out[2]_and_out[2]_not_in[0]_wire_in[1] (out[2]_and_out[2]_not_in[0]_wire_in[1]_wire, out[2]_not_in[0]_wire, in[1]);
	and2$ out[3]_and_in[1]_in[0] (out[3]_and_in[1]_in[0]_wire, in[1], in[0]);

	wire val;

	assign val = 1'b1;

	dff$ dff_out[0] (clk, out[0]_not_in[1]_wire, out[0], val, val);
	dff$ dff_out[1] (clk, in[0], out[1], val, val);
	dff$ dff_out[2] (clk, out[2]_and_out[2]_not_in[0]_wire_in[1]_wire, out[2], val, val);
	dff$ dff_out[3] (clk, out[3]_and_in[1]_in[0]_wire, out[3], val, val);

endmodule