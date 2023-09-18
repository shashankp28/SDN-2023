from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost, OVSKernelSwitch
from mininet.link import TCLink


class MyTopology(Topo):
    
    def __init__(self):
        Topo.__init__(self)
        
        link_params = {
                        'bw': 10,
                        'delay': '5ms',
                        'loss': 1,
                        'max_queue_size': 1000
                    }
        
        h1 = self.addHost('h1', ip="10.1.1.1/24", cls=CPULimitedHost, cpu=0.5)
        h2 = self.addHost('h2', ip="10.1.1.2/24", cls=CPULimitedHost, cpu=0.5)
        h3 = self.addHost('h3', ip="10.1.1.3/24", cls=CPULimitedHost, cpu=0.5)
        h4 = self.addHost('h4', ip="10.1.1.4/24", cls=CPULimitedHost, cpu=0.5)
        h5 = self.addHost('h5', ip="10.1.1.5/24", cls=CPULimitedHost, cpu=0.5)
        h6 = self.addHost('h6', ip="10.1.1.6/24", cls=CPULimitedHost, cpu=0.5)
        h7 = self.addHost('h7', ip="10.1.1.7/24", cls=CPULimitedHost, cpu=0.5)
        h8 = self.addHost('h8', ip="10.1.1.8/24", cls=CPULimitedHost, cpu=0.5)
        
        c1 = self.addSwitch('c1')
        a1 = self.addSwitch('a1')
        a2 = self.addSwitch('a2')
        e1 = self.addSwitch('e1')
        e2 = self.addSwitch('e2')
        e3 = self.addSwitch('e3')
        e4 = self.addSwitch('e4')
        
        self.addLink(c1, a1, cls=TCLink, **link_params)
        self.addLink(c1, a2, cls=TCLink, **link_params)
        self.addLink(a1, e1, cls=TCLink, **link_params)
        self.addLink(a1, e2, cls=TCLink, **link_params)
        self.addLink(a2, e3, cls=TCLink, **link_params)
        self.addLink(a2, e4, cls=TCLink, **link_params)
        self.addLink(e1, h1, cls=TCLink, **link_params)
        self.addLink(e1, h2, cls=TCLink, **link_params)
        self.addLink(e2, h3, cls=TCLink, **link_params)
        self.addLink(e2, h4, cls=TCLink, **link_params)
        self.addLink(e3, h5, cls=TCLink, **link_params)
        self.addLink(e3, h6, cls=TCLink, **link_params)
        self.addLink(e4, h7, cls=TCLink, **link_params)
        self.addLink(e4, h8, cls=TCLink, **link_params)
        

topo = MyTopology()
net = Mininet(
    topo=topo,
    switch=OVSKernelSwitch,
    autoSetMacs=True
)
net.start()
# CLI(net)
hosts = net.hosts
print("------------------ Average Ping ---------------------")
print()
results = net.pingFull()
for h1, h2, result in results:
    print(h1.name, " -> ", h2.name, ": ", result[3], "ms")
# print(net.pingFull())
net.stop()