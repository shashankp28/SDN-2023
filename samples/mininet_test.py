"""
Sample Topology for SDN class
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI

class SampleTopology( Topo ):
    """
    Custom topology for SDN class
    """
    def __init__( self ):
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        host3 = self.addHost( 'h3' )
        host4 = self.addHost( 'h4' )
        host5 = self.addHost( 'h5' )
        host6 = self.addHost( 'h6' )
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')

        # Add links Switch-Switch
        self.addLink( switch1, switch2 )
        self.addLink( switch1, switch3 )
        self.addLink( switch2, switch3 )
        self.addLink( switch2, switch4 )
        self.addLink( switch3, switch4 )

        # Add links Switch-Host
        self.addLink( switch4, host1 )
        self.addLink( switch4, host2 )
        self.addLink( switch2, host3 )
        self.addLink( switch3, host4 )
        self.addLink( switch3, host5 )
        self.addLink( switch1, host6 )

def run_topology():
    """
    Function to setup and run the topology
    """
    topo = SampleTopology()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='localhost' ),
        switch=OVSSwitch,
        autoSetMacs=True )
    net.start()
    CLI(net)
    net.stop()

if __name__=="__main__":
    run_topology()
