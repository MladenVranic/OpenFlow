from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch,Node
import json


#router class
class Router( Node ):


    #router config
    def config( self, **params ):
        #enable forwarding
        self.cmd('sysctl net.ipv4.ip_forward=1')

    #kill
    def killRouting():
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super( Router, self).killRouting()


class FrankfurtTopo( Topo ):
    #method for adding switches
    def addSwitch(self,name , **opts):
        kwargs = {'protocols': 'OpenFlow13'}
        kwargs.update(opts)
        return super(FrankfurtTopo,self).addSwitch(name,**kwargs)
    
    def __init__(self):

        Topo.__init__(self)

        #create router
        router = self.addNode('r0', cls=Router , ip='172.16.0.0/16')
        
        #open json- host file
        jsonHosts = open('hosts.json')
        jsonHosts = json.load(jsonHosts)
        #print(jsonData)

        #open json switch file
        jsonSwitches = open('switches.json')
        jsonSwitches = json.load(jsonSwitches)

        #add switches 
        firstSwitch = self.addSwitch(jsonSwitches['switchesFirstFloor'][0])
        secondSwitch = self.addSwitch(jsonSwitches['switchesSecondFloor'][0])
        thirdSwitch = self.addSwitch(jsonSwitches['switchesThirdFloor'][0])  
        
        #add router
        self.addLink(firstSwitch, router, intfName2='r0-eth1',params2={'ip': '172.16.10.0/16'})
        

        ##add hosts from Json
        for host in jsonHosts['firstFloor']:
            self.addHost(host)
            
        for host in jsonHosts['secondFloor']:
            self.addHost(host) 
    
        for host in jsonHosts['thirdFloor']:
            self.addHost(host)


        self.addLink(firstSwitch,secondSwitch)
        self.addLink(secondSwitch,thirdSwitch)

        #add Links between hosts and switches
        for host in jsonHosts['firstFloor']:
            self.addLink(host,firstSwitch)
        
        for host in jsonHosts['secondFloor']:
            self.addLink(host,secondSwitch)

        for host in jsonHosts['thirdFloor']:
            self.addLink(host,thirdSwitch)
    
        
if __name__ == '__main__':
    #create instance of topo class
    c = RemoteController('c','10.0.2.15',6653 )
    topo = FrankfurtTopo()
    net = Mininet(topo=topo, controller = None, ipBase='172.16.0.0/16')
    net.addController(c)
    net.start()
    net.pingAll() 
    CLI(net)
    net.stop()

