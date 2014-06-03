import Gnuplot
import sys
import os

x = sys.argv[1]
iters = int(x)

i = 0
ants = {}
filenames = os.listdir('../positions')
filenames.sort()

for filename in filenames:
    if filename.startswith('langtons_ant_positions') and i < iters:
        with open('../positions/' + filename) as f:
            content = f.read().splitlines()
            for line in content:
                args = line.split(' ')
                agentNr = (args[0].split('.')[0]) + args[0].split('.')[2]
                xPos = int(args[1])
                yPos = int(args[2])

                if agentNr in ants.keys():
                    ants[agentNr].append([xPos, yPos])
                else:
                    ants[agentNr] = [[xPos, yPos]]
        i += 1

g = Gnuplot.Gnuplot()
g.title('State after ' + x + ' iterations')
#g('set grid')
g.plot(*ants.values())
raw_input('Please press return to continue...\n')
