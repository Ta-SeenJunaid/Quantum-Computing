OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

reset q[0];
reset q[1];
reset q[2];
reset q[3];
h q[0];
h q[1];
ccx q[0],q[1],q[2];
cx q[0],q[3];
cx q[1],q[3];