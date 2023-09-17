sudo ovs-vsctl show

sudo ovs-ofctl -O OpenFlow13 dump-flows s1

sudo ovs-ofctl --protocols OpenFlow13 dump-flows s1



sudo ovs-vsctl show
8ba60966-6a3b-4696-884d-745a1ab733b4
 ovs_version: "2.13.0"

ls /sys/class/net
enp0s3 enp0s4 lo

sudo ovs-vsctl add-br s1

sudo ovs-vsctl add-port s1 enp0s3

sudo ovs-vsctl add-port s1 enp0s4

sudo ovs-vsctl set-controller s1 tcp:192.168.2.20:6633

sudo ovs-ofctl add-flow s1 actions=NORMAL
sudo ovs-ofctl del-flows s1
sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2
sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1
sudo ovs-vsctl del-br s1
sudo ovs-vsctl show

8ba60966-6a3b-4696-884d-745a1ab733b4
 ovs_version: "2.13.0"