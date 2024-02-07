module comb_logic (input in[1],
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
	assign out[0] = out[0]_not_in[1]_wire;
	assign out[1] = in[0];
	assign out[2] = out[2]_and_out[2]_not_in[0]_wire_in[1]_wire;
	assign out[3] = out[3]_and_in[1]_in[0]_wire;

endmodule