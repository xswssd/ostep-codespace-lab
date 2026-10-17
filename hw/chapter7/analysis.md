# Chapter 7 CPU Scheduling 분석

학번: 23217474
이름: 시에지위엔

이번 과제는 scheduler.py로 FIFO, SJF, RR 세 가지 스케줄링을 비교하는 내용이다.
응답 시간은 작업이 도착한 후 처음 CPU를 받는 시간이고, 반환 시간은 도착부터 완료까지 걸린 시간이다.

계산 문제는 먼저 -c 없이 답을 예측하고, 그 다음 -c로 시뮬레이터 결과를 확인했다.
원본 출력은 data 폴더에 저장했다.


## Q1. 작업 길이 200, 200, 200 — FIFO와 SJF 비교

명령:
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 200,200,200 -p FIFO -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 200,200,200 -p SJF -c

출력 파일: data/q1_fifo.txt, data/q1_sjf.txt

예측:
세 작업 길이가 모두 200이라서 SJF가 뭘 먼저 실행해도 결과가 같다. FIFO랑 순서가 똑같을 것이다.

Job 0: Response 0, Turnaround 200
Job 1: Response 200, Turnaround 400
Job 2: Response 400, Turnaround 600
평균 Response 200, 평균 Turnaround 400

검증:
FIFO — 평균 Response 200.00, 평균 Turnaround 400.00
SJF  — 평균 Response 200.00, 평균 Turnaround 400.00

예측이 맞았다. 작업 길이가 같으면 FIFO와 SJF는 같은 결과가 나온다.


## Q2. 작업 길이 100, 200, 300, FIFO와 SJF 비교

명령:
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,200,300 -p FIFO -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,200,300 -p SJF -c

출력 파일: data/q2_fifo.txt, data/q2_sjf.txt

예측:
작업이 이미 짧은 것부터 긴 것 순서로 들어온다. SJF도 가장 짧은 작업부터 실행하니까 FIFO와 같은 순서가 될 것이다.

Job 0: Response 0, Turnaround 100
Job 1: Response 100, Turnaround 300
Job 2: Response 300, Turnaround 600
평균 Response 133.33, 평균 Turnaround 333.33

검증:
FIFO, 평균 Response 133.33, 평균 Turnaround 333.33
SJF, 평균 Response 133.33, 평균 Turnaround 333.33

예측과 같다. 도착 순서가 이미 길이 순이면 SJF랑 FIFO 결과가 같다.


## Q3. 작업 길이 100, 200, 300, RR quantum = 1

명령:
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,200,300 -p RR -q 1 -c

출력 파일: data/q3_rr_q1.txt

예측:
quantum이 1이면 1초마다 작업이 바뀐다. Job 0, 1, 2 순서로 돌아가면서 실행된다.

Job 0: Response 0, Turnaround 298
Job 1: Response 1, Turnaround 499
Job 2: Response 2, Turnaround 600
평균 Response 1.00, 평균 Turnaround 465.67

검증:
RR q=1, 평균 Response 1.00, 평균 Turnaround 465.67

예측이 맞았다. RR은 응답 시간이 매우 낮지만 자주 바뀌어서 반환 시간은 FIFO나 SJF보다 크다.


## Q4. SJF와 FIFO의 Turnaround이 같은 경우

두 가지 경우를 생각할 수 있다.

첫째, 모든 작업 길이가 같을 때. Q1에서 봤는데 세 작업이 모두 200이면 SJF가 순서를 바꿀 이유가 없다.

둘째, 작업이 짧은 것부터 긴 것 순서로 도착할 때. Q2처럼 100, 200, 300 순서로 들어오면 SJF도 FIFO와 같은 순서로 실행한다.

정리하면 SJF가 FIFO의 실행 순서를 바꾸지 않을 때 Turnaround이 같다.


## Q5. SJF와 RR의 Response가 같은 경우

가장 명확한 경우는 모든 작업 길이가 같고 quantum이 작업 길이와 같을 때다.

예를 들어 세 작업이 모두 길이 10이고 quantum도 10이면 RR에서 각 작업이 한 번에 끝난다. Job 0은 0초, Job 1은 10초, Job 2는 20초에 첫 실행이라 Response가 0, 10, 20이다. SJF도 같은 순서로 실행해서 Response가 0, 10, 20이다.

작업이 하나만 있을 때도 같다. 어떤 정책이든 바로 실행되니까 Response는 0이다.

정리하면 작업 길이가 같고 quantum이 작업 길이와 같을 때 SJF와 RR의 Response가 같다.


## Q6. SJF에서 작업이 길어지면 Response는 어떻게 변하는가

예측:
SJF는 비선점형이라 앞 작업이 끝날 때까지 다음 작업은 기다린다. 작업이 길어지면 뒤에 있는 작업들이 더 오래 기다리니까 평균 Response도 커질 것이다.

시뮬레이터로 확인:
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 20,20,20 -p SJF -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 50,50,50 -p SJF -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,100,100 -p SJF -c

출력 파일: data/q6_sjf_20.txt, data/q6_sjf_50.txt, data/q6_sjf_100.txt

결과:
길이 20,20,20, 평균 Response 20.00
길이 50,50,50, 평균 Response 50.00
길이 100,100,100, 평균 Response 100.00

작업 길이가 커지면 평균 Response도 같이 커진다.


## Q7. RR에서 quantum이 커지면 Response는 어떻게 변하는가

예측:
quantum이 크면 각 작업이 첫 실행까지 더 오래 기다린다. 그래서 평균 Response가 커질 것이다.

시뮬레이터로 확인:
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 10,10,10 -p RR -q 1 -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 10,10,10 -p RR -q 5 -c
python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 10,10,10 -p RR -q 10 -c

출력 파일: data/q7_rr_q1.txt, data/q7_rr_q5.txt, data/q7_rr_q10.txt

결과:
quantum 1, 평균 Response 1.00, 평균 Turnaround 29.00
quantum 5, 평균 Response 5.00, 평균 Turnaround 25.00
quantum 10, 평균 Response 10.00, 평균 Turnaround 20.00

quantum이 작으면 응답은 빠르지만 자주 바뀌어서 반환 시간이 길다. quantum이 크면 응답은 느려지지만 반환 시간은 줄어든다.

N개 작업이 동시에 도착하고 모두 같은 길이일 때 가장 늦게 첫 실행하는 작업의 Response는 (N-1) x q이다. q는 quantum, N은 작업 수다.

예: N=3, q=10이면 (3-1) x 10 = 20, Job 2 Response 20.00
예: N=3, q=5이면 (3-1) x 5 = 10, Job 2 Response 10.00


## 결론

이번 과제에서 FIFO, SJF, RR 세 정책을 비교했다. 계산 문제는 먼저 예측하고 시뮬레이터로 확인했는데 모두 일치했다.

FIFO는 단순하고 공정하지만 긴 작업이 앞에 있으면 뒤 작업이 오래 기다린다.
SJF는 평균 반환 시간이 좋지만 작업 길이를 미리 알아야 하고 긴 작업은 계속 밀릴 수 있다.
RR은 응답 시간이 빨라서 인터랙티브한 시스템에 좋지만 quantum 크기를 잘 골라야 한다.

시뮬레이터 원본 출력은 hw/chapter7/data/ 폴더에 있다.
