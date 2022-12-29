#all the classes I used previously. Don't use it anymore. 


class Flow:
    def __init__(self, srcIP, dstIP, srcPort, dstPort, direction):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.direction = direction

    def __hash__(self):
        return hash((self.srcIP, self.dstIP, self.srcPort, self.dstPort, self.direction))

    def __eq__(self, other):
        if self.srcIP == other.srcIP and self.dstIP == other.dstIP and self.srcPort == other.srcPort and self.dstPort == other.dstPort and self.direction == other.direction:
            return True
        else:
            return False

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)
    
    def __str__(self):
        return f"{self.srcIP}_{self.dstIP}_{self.srcPort}_{self.dstPort}"

class Burst:
    def __init__(self, flow, pkts):
        self.flow = flow
        self.packets = pkts

    def __hash__(self):
        return hash((self.flow, self.packets[0]))

    def __eq__(self, other):
        if self.flow == other.flow and self.packets[0] == other.packets[0]:
            return True
        else:
            return False

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)
    
    def __str__(self):
        return f"{self.flow} started at {self.packets[0].time}\n"