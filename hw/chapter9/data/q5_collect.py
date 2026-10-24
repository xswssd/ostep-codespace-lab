import re
import subprocess
import os

os.chdir('/workspaces/ostep-codespace-lab/ext/ostep-homework/cpu-sched-lottery')
D = '/workspaces/ostep-codespace-lab/hw/chapter9/data'

with open(D + '/q5-fairness-data.txt', 'w') as out:
    for R in [1, 10, 50, 100, 500, 1000]:
        Fs = []
        for s in range(30):
            result = subprocess.run(
                ['./lottery.py', '-l', f'{R}:100,{R}:100', '-s', str(s), '-c'],
                capture_output=True, text=True)
            times = {
                int(m.group(1)): int(m.group(2))
                for m in re.finditer(r'JOB (\d) DONE at time (\d+)', result.stdout)
            }
            j0, j1 = times[0], times[1]
            F = min(j0, j1) / max(j0, j1)
            Fs.append(F)
            out.write(f'R={R} seed={s} J0={j0} J1={j1} F={F:.4f}\n')
        avg = sum(Fs) / len(Fs)
        out.write(f'R={R} AVG_F={avg:.4f}\n\n')
        out.flush()
        print(f'R={R} AVG_F={avg:.4f}')

print('Q5DONE')
