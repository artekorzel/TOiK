import Gnuplot
import sys
import os

x = sys.argv[1]
iters = int(x)

i = 0
ants = {}
for filename in os.listdir('positions'):
    if i < iters:
        with open('positions/' + filename) as f:
            content = f.read().splitlines()
            for line in content:
                args = line.split(' ')
                agentNr = int(args[0].split('.')[0])
                xPos = int(args[1])
                yPos = int(args[2])

                if agentNr in ants.keys():
                    ants[agentNr].append([xPos, yPos])
                else:
                    ants[agentNr] = [[xPos, yPos]]
        i += 1

g = Gnuplot.Gnuplot()
g.title('State after ' + x + ' iterations')
d = []
for path in ants.values():
    d.append(Gnuplot.Data(path))
#g('set grid')
g.plot(*ants.values())
raw_input('Please press return to continue...\n')
