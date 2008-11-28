import os

def startup():
	os.system("brctl addbr br0")
	os.system("brctl stp br0 off")
	os.system("brctl addif br0 eth1")
	os.system("brctl addif br0 eth2")
	os.system("ifconfig eth1 down")
	os.system("ifconfig eth2 down")
	os.system("ifconfig eth1 0.0.0.0 up")
	os.system("ifconfig eth2 0.0.0.0 up")
	os.system("ifconfig br0 0.0.0.0 up")

