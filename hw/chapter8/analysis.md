# Chapter 8 MLFQ 분석

학번: 23217474
이름: 시에지위엔

Q1: 2 jobs, 2 queues, I/O 없음. 먼저 예측 후 -c로 검증.

## Seed 0 (Job0:17ms, Job1:8ms)
- Job0가 Priority1에서 10ms 후 강등, Job1이 Priority1에서 8ms 실행
- Job0 response=0 turnaround=25, Job1 response=10 turnaround=18
- 출력: data/q1-seed0.txt

## Seed 1 (Job0:3ms, Job1:15ms)
- Job0가 3ms만 실행 후 종료, Job1이 time3부터 시작
- Job0 response=0 turnaround=3, Job1 response=3 turnaround=18
- 출력: data/q1-seed1.txt

## Seed 2 (Job0:19ms, Job1:2ms)
- Seed0와 유사, Job1은 time10에 2ms만 실행
- Job0 response=0 turnaround=21, Job1 response=10 turnaround=12
- 출력: data/q1-seed2.txt

모든 예측이 시뮬레이터 결과와 일치했다.
