from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

from ryu.topology.api import get_switch
from ryu.topology import event 
from collections import deque

class Graph:
    def __init__(self):
        self.nodes = dict()

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()

    def add_edge(self, src, dst, attr=None):
        if src not in self.nodes:
            self.edges[src] = set()
        self.nodes[src].add((dst, attr))

    def add_nodes_from(self, nodes):
        for node in nodes:
            self.add_node(node)
    
    def add_edges_from(self, edges):
        for edge in edges:
            self.add_edge(*edge)
    
    def get_out_port(self, dpid, hop):
        if dpid in self.nodes and hop in self.nodes[dpid]:
            for _, attr in self.nodes[dpid][hop]:
                port = attr
                if port is not None:
                    return port
        return None
    
    def shortest_path(self, src, dst):
        if src not in self.nodes or dst not in self.nodes:
            return None

        visited = set()
        queue = deque([(src, [])])

        while queue:
            current_node, path = queue.popleft()
            visited.add(current_node)

            if current_node == dst:
                return path + [current_node]

            for neighbor, _ in self.nodes[current_node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_node]))

        return None
    
    def __contains__(self, node):
        return node in self.nodes


class ShortestPathController(app_manager.RyuApp):
	
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ShortestPathController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.net=Graph()
        self.nodes = {}
        self.links = {}
        self.no_of_nodes = 0
        self.no_of_links = 0
        self.i=0

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port, dl_dst=haddr_to_bin(dst))

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        print("---------------------------")
        print(self.net.nodes)
        print()
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        if src not in self.net:
            self.net.add_node(src)
            self.net.add_edge(dpid,src, msg.in_port)
            self.net.add_edge(src,dpid)
        if dst in self.net:
            path=self.net.shortest_path(src, dst)
            hop=path[path.index(dpid)+1]
            out_port=self.net.get_out_port(dpid, hop)
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]


        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self.topology_api_app, None)
        switches=[switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches)
        print("----------------------")
        print( "List of Nodes", self.net.nodes )
