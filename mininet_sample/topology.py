from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch
import subprocess

class MyTopology(Topo):
    
    def __init__(self):
        Topo.__init__(self)
        
        host1 = self.addHost('h1', ip="10.1.1.1/24")
        host2 = self.addHost('h2', ip="10.1.1.2/24")
        
        switch1 = self.addSwitch('s1', dpid="0000000000000099", listen=6633)
        
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        

topo = MyTopology()
net = Mininet(
    topo=topo,
    controller=lambda name: RemoteController(name, ip='172.17.0.3', port=6633),
    switch=OVSSwitch,
    autoSetMacs=True
)
net.start()
CLI(net)
net.stop()