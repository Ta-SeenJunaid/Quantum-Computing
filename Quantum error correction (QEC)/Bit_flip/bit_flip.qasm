OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

reset q[0];
reset q[1];
reset q[2];
barrier q[0],q[1],q[2];
cx q[0],q[1];
ccx q[0],q[1],q[2];
barrier q[0],q[1],q[2];
x q[0];
barrier q[0],q[1],q[2];
cx q[0],q[1];
cx q[0],q[2];
ccx q[2],q[1],q[0];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];