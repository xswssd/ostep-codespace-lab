# OSTEP Ch.4 Homework Answers
## Q1
- Prediction: Both processes are CPU-only (5:100,5:100) and never issue any I/O. The scheduler only switches when the current process finishes or issues an I/O, so PID0 runs its 5 ticks first, then PID1 runs its 5 ticks. The CPU is never idle. Total time 10, CPU utilization 100%.
```
Time PID 0    PID 1    CPU IOs
1    RUN:cpu  READY    1
2    RUN:cpu  READY    1
3    RUN:cpu  READY    1
4    RUN:cpu  READY    1
5    RUN:cpu  READY    1
6    DONE     RUN:cpu  1
7    DONE     RUN:cpu  1
8    DONE     RUN:cpu  1
9    DONE     RUN:cpu  1
10   DONE     RUN:cpu  1
```
- Reasoning: Both processes are pure CPU-bound (Y=100), so they never enter BLOCKED. The CPU column is 1 for all 10 ticks, giving 100% utilization; total time = 5+5 = 10.

## Q2
- Prediction: PID0 runs 4 CPU instructions (4:100) for ticks 1-4; PID1 (1:0) does a single I/O: RUN:io takes 1 tick, then BLOCKED for 5 ticks, then RUN:io_done takes 1 tick. PID1 only starts after PID0 finishes, and the CPU idles while PID1 blocks. Total time 11, CPU utilization 6/11 ~= 54.55%.
```
Time PID 0    PID 1      CPU IOs
1    RUN:cpu  READY      1
2    RUN:cpu  READY      1
3    RUN:cpu  READY      1
4    RUN:cpu  READY      1
5    DONE     RUN:io     1
6    DONE     BLOCKED         1
7    DONE     BLOCKED         1
8    DONE     BLOCKED         1
9    DONE     BLOCKED         1
10   DONE     BLOCKED         1
11   DONE     RUN:io_done 1
```
- Reasoning: One I/O costs 3 CPU ticks (RUN:io + RUN:io_done) plus 5 BLOCKED ticks. PID0 uses 4 ticks, PID1 uses 6 ticks, but they run serially without overlap, so total is 11 ticks. The CPU is idle only during PID1's 5 blocked ticks.

## Q3
- Prediction: PID0 (1:0) issues I/O first; with the default SWITCH_ON_IO the scheduler immediately switches to PID1. PID1's 4 CPU instructions run during PID0's blocked period (ticks 2-5), so the CPU is never idle. PID0's I/O completes at tick 7. Total time 7, CPU utilization 6/7 ~= 85.71%.
```
Time PID 0      PID 1    CPU IOs
1    RUN:io     READY    1
2    BLOCKED    RUN:cpu  1    1
3    BLOCKED    RUN:cpu  1    1
4    BLOCKED    RUN:cpu  1    1
5    BLOCKED    RUN:cpu  1    1
6    BLOCKED    DONE         1
7*   RUN:io_done DONE    1
```
- Reasoning: Same processes as Q2 but in opposite order. The process that issues I/O runs first; while it blocks, the other CPU process immediately takes over. Only tick 6 (PID1 done, PID0 not yet finished) leaves the CPU idle for 1 tick.

## Q4
- Prediction: Same processes as Q3, but with -S SWITCH_ON_END: the scheduler does NOT switch when a process issues I/O. After PID0 enters BLOCKED the CPU simply waits idle; PID1 only gets the CPU after PID0 fully finishes (tick 7), running ticks 8-11. Total time 11, CPU utilization 6/11 ~= 54.55%.
```
Time PID 0      PID 1    CPU IOs
1    RUN:io     READY    1
2    BLOCKED    READY         1
3    BLOCKED    READY         1
4    BLOCKED    READY         1
5    BLOCKED    READY         1
6    BLOCKED    READY         1
7*   RUN:io_done READY   1
8    DONE       RUN:cpu  1
9    DONE       RUN:cpu  1
10   DONE       RUN:cpu  1
11   DONE       RUN:cpu  1
```
- Reasoning: SWITCH_ON_END only switches when the current process "finishes"; issuing an I/O does not count as finishing, so the CPU spins idle during PID0's 5 blocked ticks.

## Q5
- Prediction: Same processes as Q3/Q4, but using the default -S SWITCH_ON_IO (i.e. the Q3 setting). The result is identical to Q3: total time 7, CPU utilization 85.71%.
```
Time PID 0      PID 1    CPU IOs
1    RUN:io     READY    1
2    BLOCKED    RUN:cpu  1    1
3    BLOCKED    RUN:cpu  1    1
4    BLOCKED    RUN:cpu  1    1
5    BLOCKED    RUN:cpu  1    1
6    BLOCKED    DONE         1
7*   RUN:io_done DONE    1
```
- Reasoning: SWITCH_ON_IO switches when an I/O is issued, letting PID1 use the CPU during the blocking period; this contrasts with Q4's SWITCH_ON_END.

## Q6
- Prediction: Four processes (PID0 does 3 I/Os, PID1-3 each run 5 CPU instructions), with -S SWITCH_ON_IO -I IO_RUN_LATER. After PID0's first I/O it switches to PID1-3 which each run their 5 CPU instructions; when the I/O finishes PID0 returns to READY but must wait its turn (IO_RUN_LATER), so its 3 I/Os are spread out and the I/O device sits idle for long stretches while the CPUs are busy. Predict total time is fairly long (about 31 ticks), CPU utilization moderate (about 68%).
```
Time PID 0    PID 1    PID 2    PID 3    CPU IOs
1    RUN:io   READY    READY    READY    1
2    BLOCKED  RUN:cpu  READY    READY    1    1
3    BLOCKED  RUN:cpu  READY    READY    1    1
4    BLOCKED  RUN:cpu  READY    READY    1    1
5    BLOCKED  RUN:cpu  READY    READY    1    1
6    BLOCKED  RUN:cpu  READY    READY    1    1
7*   READY    DONE     RUN:cpu  READY    1
8    READY    DONE     RUN:cpu  READY    1
9    READY    DONE     RUN:cpu  READY    1
10   READY    DONE     RUN:cpu  READY    1
11   READY    DONE     RUN:cpu  READY    1
12   READY    DONE     DONE     RUN:cpu  1
13   READY    DONE     DONE     RUN:cpu  1
14   READY    DONE     DONE     RUN:cpu  1
15   READY    DONE     DONE     RUN:cpu  1
16   READY    DONE     DONE     RUN:cpu  1
17   RUN:io_done DONE   DONE     DONE    1
18   RUN:io   DONE     DONE     DONE    1
19   BLOCKED  DONE     DONE     DONE         1
20   BLOCKED  DONE     DONE     DONE         1
21   BLOCKED  DONE     DONE     DONE         1
22   BLOCKED  DONE     DONE     DONE         1
23   BLOCKED  DONE     DONE     DONE         1
24*  RUN:io_done DONE   DONE     DONE    1
25   RUN:io   DONE     DONE     DONE    1
26   BLOCKED  DONE     DONE     DONE         1
27   BLOCKED  DONE     DONE     DONE         1
28   BLOCKED  DONE     DONE     DONE         1
29   BLOCKED  DONE     DONE     DONE         1
30   BLOCKED  DONE     DONE     DONE         1
31*  RUN:io_done DONE   DONE     DONE    1
```
- Reasoning: IO_RUN_LATER means PID0 cannot immediately resume after its I/O completes; it must wait until the other processes have their turn. So a lot of CPU work (PID1-3) is inserted between its 3 I/Os, and the I/O device is idle for many ticks.

## Q7
- Prediction: Same processes as Q6 and -S SWITCH_ON_IO, but with -I IO_RUN_IMMEDIATE: each time PID0's I/O completes it runs again immediately, so its 3 I/Os happen back-to-back and the CPU is always busy with PID0's RUN:io_done/RUN:io during the I/O gaps. Predict total time 21, CPU utilization 100%.
```
Time PID 0    PID 1    PID 2    PID 3    CPU IOs
1    RUN:io   READY    READY    READY    1
2    BLOCKED  RUN:cpu  READY    READY    1    1
3    BLOCKED  RUN:cpu  READY    READY    1    1
4    BLOCKED  RUN:cpu  READY    READY    1    1
5    BLOCKED  RUN:cpu  READY    READY    1    1
6    BLOCKED  RUN:cpu  READY    READY    1    1
7*   RUN:io_done DONE   READY    READY    1
8    RUN:io   DONE     READY    READY    1
9    BLOCKED  DONE     RUN:cpu  READY    1    1
10   BLOCKED  DONE     RUN:cpu  READY    1    1
11   BLOCKED  DONE     RUN:cpu  READY    1    1
12   BLOCKED  DONE     RUN:cpu  READY    1    1
13   BLOCKED  DONE     RUN:cpu  READY    1    1
14*  RUN:io_done DONE   DONE     READY    1
15   RUN:io   DONE     DONE     READY    1
16   BLOCKED  DONE     DONE     RUN:cpu  1    1
17   BLOCKED  DONE     DONE     RUN:cpu  1    1
18   BLOCKED  DONE     DONE     RUN:cpu  1    1
19   BLOCKED  DONE     DONE     RUN:cpu  1    1
20   BLOCKED  DONE     DONE     RUN:cpu  1    1
21*  RUN:io_done DONE   DONE     DONE    1
```
- Reasoning: IO_RUN_IMMEDIATE lets the I/O-heavy process "jump the queue" and resume right away, so its 3 I/Os run consecutively with no idle CPU tick; total time is much shorter than Q6.

## Q8
- Prediction: -s 1/2/3 -l 3:50,3:50. First predict from the instruction list, then compare the effect of -I IO_RUN_IMMEDIATE and -S SWITCH_ON_END. Intuition: -S SWITCH_ON_END is worst (the I/O process is not switched out, so the other process must wait for it to finish entirely); -I IO_RUN_IMMEDIATE should let the I/O process resume promptly and shorten total time.
- Reasoning: Each process has 3 instructions, each 50% likely to be CPU or I/O. The default SWITCH_ON_IO switches on I/O; SWITCH_ON_END forces serial execution; IO_RUN_IMMEDIATE lets the I/O completer jump the queue. The instruction sequences differ per seed, but the trend of the conclusions should be the same.
