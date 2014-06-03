import os

dirs = os.listdir('.')
dirs.sort()

if not 'result' in dirs:
    os.mkdir('result')

for dir in dirs:
    if dir != 'merge.py' and dir != 'result':
        dir += '/positions/'
        filenames = os.listdir(dir)
        filenames.sort()
        for filename in filenames:
            if filename.startswith('langtons_ant_positions'):
                with open(dir + filename) as f:
                    content = f.read().splitlines()
                    for line in content:
                        val = 'result/' + filename
                        with open(val, "a") as file:
                            file.write(line + '\n')