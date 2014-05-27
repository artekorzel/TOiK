

class BorderType:
    N = 1
    S = 2
    E = 3
    W = 4


class Border:
    def __init__(self, xSize, ySize):
        self.N = [[[] for _ in range(xSize)] for _ in range(2)]
        self.S = [[[] for _ in range(xSize)] for _ in range(2)]
        self.E = [[[] for _ in range(ySize)] for _ in range(2)]
        self.W = [[[] for _ in range(ySize)] for _ in range(2)]
        self.xSize = xSize
        self.ySize = ySize

    def clear(self):
        self.N = [[[] for _ in range(self.xSize)] for _ in range(2)]
        self.S = [[[] for _ in range(self.xSize)] for _ in range(2)]
        self.E = [[[] for _ in range(self.ySize)] for _ in range(2)]
        self.W = [[[] for _ in range(self.ySize)] for _ in range(2)]

    def checkForAgent(self, border, x, y):
        if x < 2 and y < len(border):
            return not border[y][x]
        return False

    def addAgentsToBorder(self, border, agents, row):
        for agent in agents:
            if agent < len(border):
                border[row][agent].append(agent)

    def containsAgent(self, borderType, x, y):
        if borderType == BorderType.N:
            return self.checkForAgent(self.N, x, y)
        if borderType == BorderType.S:
            return self.checkForAgent(self.S, x, y)
        if borderType == BorderType.E:
            return self.checkForAgent(self.E, x, y)
        if borderType == BorderType.W:
            return self.checkForAgent(self.W, x, y)

    def addAgents(self, borderType, agents):
        if borderType == BorderType.N:
            self.addAgentsToBorder(self.N, agents[0], 0)
            self.addAgentsToBorder(self.N, agents[1], 1)
        if borderType == BorderType.S:
            self.addAgentsToBorder(self.S, agents[0], 0)
            self.addAgentsToBorder(self.S, agents[1], 1)
        if borderType == BorderType.E:
            self.addAgentsToBorder(self.W, agents[0], 0)
            self.addAgentsToBorder(self.W, agents[1], 1)
        if borderType == BorderType.W:
            self.addAgentsToBorder(self.E, agents[0], 0)
            self.addAgentsToBorder(self.E, agents[1], 1)

    def printBordes(self):
        print "N:" + str(self.N[0]) + "\t" + str(self.N[1])
        print "S:" + str(self.S[0]) + "\t" + str(self.S[1])
        print "E:" + str(self.E[0]) + "\t" + str(self.E[1])
        print "W:" + str(self.W[0]) + "\t" + str(self.W[1])