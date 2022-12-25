from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController


class FrankfurtTopo( Topo ):
    #method for adding switches
    def addSwitch(self.name , **opts):
        kwargs = {'protocols', 'OpenFlow13'}
        kwargs.update(opts)
        return super(FrankfurtTopo,self).addSwitch(name,**kwargs)
    
    def __init__():

        Topo.__init__(self)

        #add switches 
        firstSwitch = self.addSwitch('s1')
        secondSwitch = self.addSwitch('s2')
        thirdSwitch = self.addSwitch('s3')
        
        #host arrays
        hostsFirstFloor = ['h1','h2','h3','h4','h5']
        hostsSecondFloor = ['h6','h7','h8','h9','10']
        hostsThirdFloor = ['h11','h12','h13','h14','15']

        ##add hosts
        for host in hostsFirstFloor:
            self.addHost(host)

        for host in hostsSecondFloor:
            self.addHost(host)

        for host in hostsThirdFloor:
            self.addHost(host)


        self.addLink(firstSwitch,secondSwitch)
        self.addLink(secondSwitch, thirdSwitch)

        #add first floor to link
        for host in hostsFirstFloor:
            self.addLink(host,firstSwitch)
        
        for host in hostsSecondFloor:
            self.addLink(host,secondSwitch)

        for host in hoststhirdFloor:
            self.addLink(host,thirdSwitch)
        


if __name__ == '__main__':
    #create instance of topo class
    c = RemoteController('c','10.0.2.15', 6653)
    topo = FrankfurtTopo()
    net.addController(c)
    net = Mininet(topo=topo, controller = RemoteController)
    net.start()
    CLI(net)
    net.stop()

